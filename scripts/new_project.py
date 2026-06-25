"""Cria um novo projeto a partir de um profile do template.

Resolve o profile (extends + packs), copia os arquivos para o destino e,
em projetos Python, aplica o nome do pacote. Com --dry-run, mostra a
contabilidade de tokens separando contexto sempre-carregado, sob-demanda
e arquivos de projeto.

Requer apenas Python 3.11+ (usa só a biblioteca padrão). A forma mais
simples de rodar é sem argumentos — abre um assistente interativo:

    python scripts/new_project.py        (ou: novo-projeto.cmd / ./novo-projeto.sh)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from _template_lib import (
    ALWAYS_ON_BUDGET_TOKENS,
    CONTEXT_CATEGORIES,
    DEFAULT_OFF_CATEGORIES,
    PYTHON_PACK,
    ResolvedProfile,
    TemplateError,
    build_file_map,
    collect_python_requirements,
    estimate_tokens_for_file,
    list_profiles,
    render_pyproject,
    resolve_profile,
)

TEMPLATE_VERSION = "2.1"

CATEGORY_ORDER = [
    "always-on",
    "instructions",
    "skills",
    "prompts",
    "agents",
    "base",
    "build",
    "ci",
    "tests",
    "examples",
]

CATEGORY_LABEL = {
    "always-on": "Sempre carregado (always-on)",
    "instructions": "Instruções por applyTo (sob-demanda)",
    "skills": "Skills (sob-demanda)",
    "prompts": "Prompts (sob-demanda)",
    "agents": "Agents (sob-demanda)",
    "base": "Base do projeto (esqueleto, fora do contexto)",
    "build": "Build Python (pyproject/Makefile, opt-in)",
    "ci": "CI / workflows (opt-in)",
    "tests": "Testes de exemplo (opt-in)",
    "examples": "Arquivos de exemplo (opt-in)",
}


def compute_excludes(args: argparse.Namespace) -> set[str]:
    """Resolve quais categorias NÃO entram, juntando dois mecanismos:

    - Orientação .github excluível via --without-* (agents/skills/prompts).
    - Categorias OFF por padrão (build/ci/tests/examples) que só entram com --with-*.
    """
    excludes: set[str] = set()
    if args.without_agents:
        excludes.add("agents")
    if args.without_skills:
        excludes.add("skills")
    if args.without_prompts:
        excludes.add("prompts")

    off = set(DEFAULT_OFF_CATEGORIES)
    if args.with_pyproject:
        off.discard("build")
        off.discard("ci")  # CI Python acompanha o pyproject (precisa dele pra rodar)
    if args.with_tests:
        off.discard("tests")
    if args.with_examples:
        off.discard("examples")
    return excludes | off


def normalize_project_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.strip().lower()
    normalized = re.sub(r"[\s\-]+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_]", "", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    if not normalized:
        raise ValueError("Nome de projeto inválido após normalização")
    if normalized[0].isdigit():
        normalized = f"project_{normalized}"
    return normalized


def print_token_report(
    profile: ResolvedProfile,
    file_map: dict[str, tuple[Path, str]],
    target: Path,
    project_name: str,
    heading: str = "\nDRY RUN — nenhum arquivo foi copiado",
) -> None:
    stats: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "tokens": 0})
    for dest_rel, (src, category) in file_map.items():
        tokens = estimate_tokens_for_file(src)
        stats[category]["files"] += 1
        stats[category]["tokens"] += tokens

    always_on = stats["always-on"]["tokens"]
    on_demand = sum(stats[c]["tokens"] for c in CONTEXT_CATEGORIES if c != "always-on")
    out_of_context = sum(
        stats[c]["tokens"] for c in stats if c not in CONTEXT_CATEGORIES
    )

    print(heading)
    print(f"Profile: {profile.name}  ({profile.description})")
    print(f"Packs:   {' -> '.join(profile.packs)}")
    if profile.exclude_categories:
        print(f"Excluído: {', '.join(sorted(profile.exclude_categories))}")
    print(f"Destino: {target}")
    print(f"Nome normalizado: {project_name}")

    print("\n=== Orçamento de contexto do Copilot ===")
    budget_flag = "  ⚠ ACIMA DO ORÇAMENTO" if always_on > ALWAYS_ON_BUDGET_TOKENS else "  ✓"
    print(f"Sempre carregado (always-on): ~{always_on} tokens "
          f"(orçamento {ALWAYS_ON_BUDGET_TOKENS}){budget_flag}")
    print(f"Sob-demanda (instructions/skills/prompts/agents): ~{on_demand} tokens")
    print(f"Fora do contexto (projeto + CI): ~{out_of_context} tokens")

    print("\n=== Detalhe por categoria ===")
    for category in CATEGORY_ORDER:
        if category not in stats:
            continue
        s = stats[category]
        print(f"- {CATEGORY_LABEL[category]}: {s['files']} arquivo(s), ~{s['tokens']} tokens")

    print("\n=== Arquivos planejados ===")
    for dest_rel in sorted(file_map):
        print(f"- {dest_rel}")

    if always_on > ALWAYS_ON_BUDGET_TOKENS:
        print(
            "\n⚠ A camada always-on está acima do orçamento. Mova regras detalhadas "
            "para skills/instruções com applyTo para reduzir o custo por prompt."
        )


def copy_files(file_map: dict[str, tuple[Path, str]], target: Path, force: bool) -> None:
    for dest_rel in sorted(file_map):
        src, _ = file_map[dest_rel]
        destination = target / dest_rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not force:
            print(f"skip existing: {destination}")
            continue
        shutil.copy2(src, destination)
        print(f"copied: {dest_rel}")


def replace_in_file(path: Path, old: str, new: str) -> None:
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if old not in content:
        return
    path.write_text(content.replace(old, new), encoding="utf-8")
    print(f"updated: {path.name}")


def replace_token_in_text_files(target: Path, old: str, new: str) -> None:
    supported = {".py", ".md", ".toml", ".yml", ".yaml", ".txt", ".cfg"}
    for path in target.rglob("*"):
        if path.is_file() and path.suffix.lower() in supported:
            replace_in_file(path, old, new)


def compose_pyproject(target: Path, profile: ResolvedProfile) -> None:
    """Compõe o pyproject do projeto: injeta as deps declaradas pelos packs.

    O pyproject base (do pack python) traz as sentinelas; cada pack contribui
    com suas dependências via `[python]` no pack.toml.
    """
    path = target / "pyproject.toml"
    if not path.exists():
        return
    deps, groups = collect_python_requirements(profile)
    rendered = render_pyproject(path.read_text(encoding="utf-8"), deps, groups)
    path.write_text(rendered, encoding="utf-8")
    print(f"composed: pyproject.toml ({len(deps)} dep(s), {len(groups)} grupo(s))")


def apply_python_project_naming(
    target: Path, project_name: str, ensure_package: bool, force: bool
) -> None:
    src_root = target / "src"
    old_pkg = src_root / "nome_pacote"
    new_pkg = src_root / project_name
    if old_pkg.is_dir():
        if new_pkg.exists() and not force:
            print(f"skip existing package dir: {new_pkg}")
        else:
            if new_pkg.exists() and force:
                shutil.rmtree(new_pkg)
            old_pkg.rename(new_pkg)
            print(f"renamed package dir: nome_pacote -> {project_name}")
    elif ensure_package and not new_pkg.is_dir():
        # pyproject sem módulos de exemplo: cria um pacote vazio para instalar.
        new_pkg.mkdir(parents=True, exist_ok=True)
        (new_pkg / "__init__.py").write_text("", encoding="utf-8")
        print(f"created package dir: src/{project_name}/__init__.py")
    # Com um pacote real em src/, o placeholder .gitkeep não é mais necessário.
    if new_pkg.is_dir():
        gitkeep = src_root / ".gitkeep"
        if gitkeep.exists():
            gitkeep.unlink()
    replace_token_in_text_files(target, "nome_pacote", project_name)
    replace_in_file(target / "pyproject.toml", 'name = "nome-projeto"', f'name = "{project_name}"')


# Conversão pip/venv -> uv aplicada só quando o usuário pede --with-uv.
# A fonte canônica dos packs é uv-free; assim o caminho padrão (sem uv) não
# precisa de nenhuma reescrita.
_UV_TEXT_REPLACEMENTS = [
    ("pip install -e .", "uv sync"),
    ("ruff check", "uv run ruff check"),
    ("ruff format", "uv run ruff format"),
    ("pytest", "uv run pytest"),
]

_UV_WORKFLOW_INSTALL = """      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync --all-extras --dev"""

_PIP_WORKFLOW_INSTALL = """      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .
          pip install ruff pytest"""


def apply_uv_preference(target: Path) -> None:
    """Converte os comandos de setup para uv nos arquivos gerados.

    Toca README.md, AGENTS.md, Makefile e os workflows. Idempotente o bastante
    para o uso aqui (roda uma vez sobre fonte em pip/venv)."""
    for rel in ("README.md", "AGENTS.md", "Makefile"):
        path = target / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in _UV_TEXT_REPLACEMENTS:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    workflows = target / ".github" / "workflows"
    if workflows.is_dir():
        for wf in workflows.glob("*.yml"):
            text = wf.read_text(encoding="utf-8")
            if _PIP_WORKFLOW_INSTALL in text:
                text = text.replace(_PIP_WORKFLOW_INSTALL, _UV_WORKFLOW_INSTALL)
                text = text.replace("ruff check", "uv run ruff check")
                text = text.replace("ruff format", "uv run ruff format")
                text = text.replace("run: pytest", "run: uv run pytest")
                wf.write_text(text, encoding="utf-8")
    print("applied: preferência uv (comandos convertidos para uv)")


def write_project_manifest(
    target: Path, profile: ResolvedProfile, project_name: str, args: argparse.Namespace
) -> None:
    manifest = {
        "template_version": TEMPLATE_VERSION,
        "profile": profile.name,
        "packs": profile.packs,
        "project_name": project_name,
        "options": {
            "pyproject": bool(args.with_pyproject),
            "tests": bool(args.with_tests),
            "examples": bool(args.with_examples),
            "uv": bool(args.with_uv),
        },
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path = target / ".copilot-template.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote: .copilot-template.json")


def _ask(prompt: str, default: str = "") -> str:
    """input() com valor padrão exibido entre colchetes."""
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def _ask_yes_no(prompt: str, default: bool = True) -> bool:
    hint = "S/n" if default else "s/N"
    answer = _ask(f"{prompt} ({hint})").lower()
    if not answer:
        return default
    return answer in {"s", "sim", "y", "yes"}


def interactive_inputs() -> argparse.Namespace:
    """Assistente interativo: pergunta profile, nome, pasta e contexto.

    Devolve um Namespace compatível com o fluxo normal de main().
    """
    print("=" * 60)
    print("  Assistente de criação de projeto (GitHub Copilot Template)")
    print("=" * 60)

    profiles = list_profiles()
    print("\nProfiles disponíveis:")
    descriptions: dict[str, str] = {}
    for i, name in enumerate(profiles, start=1):
        try:
            prof = resolve_profile(name)
            descriptions[name] = prof.description
            print(f"  {i:>2}. {name:<16} {prof.description}")
        except TemplateError as exc:
            print(f"  {i:>2}. {name:<16} (erro: {exc})")

    profile = ""
    while not profile:
        choice = _ask("\nEscolha o profile (número ou nome)", "python")
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            profile = profiles[int(choice) - 1]
        elif choice in profiles:
            profile = choice
        else:
            print(f"  Opção inválida: {choice!r}. Tente de novo.")

    project_name = ""
    while not project_name:
        raw = _ask("Nome do projeto")
        if not raw:
            print("  O nome é obrigatório.")
            continue
        try:
            project_name = normalize_project_name(raw)
        except ValueError:
            print("  Nome inválido. Use letras/números.")
    if project_name != raw.strip():
        print(f"  (normalizado para: {project_name})")

    parent = _ask(
        "Diretório onde criar o projeto (a pasta do projeto será criada dentro dele)",
        ".",
    )
    target = str((Path(parent).expanduser() / project_name).resolve())
    print(f"  → o projeto será criado em: {target}")

    full_context = _ask_yes_no("Incluir a orientação do Copilot (agents, skills, prompts)?",
                               default=True)

    print("\nO projeto nasce enxuto (só src/ + orientação). Extras são opcionais:")
    with_pyproject = _ask_yes_no("Gerar projeto Python instalável (pyproject + Makefile + CI)?",
                                 default=False)
    with_uv = False
    if with_pyproject:
        with_uv = _ask_yes_no("Usar uv como gerenciador? (não = venv + pip)", default=False)
    with_tests = _ask_yes_no("Incluir testes de exemplo?", default=False)
    with_examples = _ask_yes_no("Incluir arquivos de exemplo (código/queries de partida)?",
                                default=False)

    print()
    return argparse.Namespace(
        profile=profile,
        target=target,
        project_name=project_name,
        without_agents=not full_context,
        without_skills=not full_context,
        without_prompts=not full_context,
        with_pyproject=with_pyproject,
        with_tests=with_tests,
        with_examples=with_examples,
        with_uv=with_uv,
        dry_run=False,
        force=False,
        list=False,
        interactive=True,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cria um projeto a partir de um profile do template.")
    parser.add_argument("--profile", help="Profile a aplicar (ver --list)")
    parser.add_argument("--target", help="Diretório destino do projeto")
    parser.add_argument("--project-name", help="Nome do projeto (normalizado para snake_case)")
    parser.add_argument("--without-agents", action="store_true",
                        help="Não inclui os agents da orientação .github")
    parser.add_argument("--without-skills", action="store_true",
                        help="Não inclui as skills da orientação .github")
    parser.add_argument("--without-prompts", action="store_true",
                        help="Não inclui os prompts da orientação .github")
    parser.add_argument("--with-pyproject", action="store_true",
                        help="Gera pyproject.toml + Makefile + CI (projeto Python instalável)")
    parser.add_argument("--with-tests", action="store_true",
                        help="Inclui testes de exemplo (e a orientação de testes)")
    parser.add_argument("--with-examples", action="store_true",
                        help="Inclui código/queries de exemplo dos packs")
    parser.add_argument("--with-uv", action="store_true",
                        help="Usa uv nos comandos gerados (padrão: venv + pip)")
    parser.add_argument("--dry-run", action="store_true", help="Mostra plano + tokens, sem gravar")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos existentes")
    parser.add_argument("--list", action="store_true", help="Lista profiles disponíveis e sai")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="Assistente interativo (também é o padrão quando rodado sem argumentos)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        print("Profiles disponíveis:")
        for name in list_profiles():
            try:
                prof = resolve_profile(name)
                print(f"- {name}: {prof.description}  [packs: {', '.join(prof.packs)}]")
            except TemplateError as exc:
                print(f"- {name}: (erro) {exc}")
        return 0

    # Sem profile/target: cai no assistente interativo (modo padrão e amigável).
    if args.interactive or (not args.profile and not args.target):
        args = interactive_inputs()
    elif not args.profile or not args.target:
        parser.error("--profile e --target são obrigatórios (ou rode sem argumentos para o assistente)")

    try:
        profile = resolve_profile(args.profile)
        file_map = build_file_map(profile, compute_excludes(args))
    except TemplateError as exc:
        print(f"ERRO: {exc}")
        return 2

    target = Path(args.target).resolve()
    project_name = normalize_project_name(args.project_name or target.name)

    if args.dry_run:
        print_token_report(profile, file_map, target, project_name)
        return 0

    # No assistente, mostra o plano + orçamento e pede confirmação antes de gravar.
    if getattr(args, "interactive", False):
        print_token_report(profile, file_map, target, project_name,
                           heading="\nPlano de criação")
        if not _ask_yes_no("\nCriar o projeto agora?", default=True):
            print("Cancelado. Nada foi gravado.")
            return 0

    target.mkdir(parents=True, exist_ok=True)
    copy_files(file_map, target, args.force)

    if PYTHON_PACK in profile.packs:
        if args.with_pyproject:
            compose_pyproject(target, profile)
        # Renomeia/cria o pacote quando há módulos de exemplo ou pyproject.
        if args.with_examples or args.with_pyproject:
            apply_python_project_naming(target, project_name, args.with_pyproject, args.force)

    if args.with_uv:
        apply_uv_preference(target)

    write_project_manifest(target, profile, project_name, args)

    print(f"\nProfile '{profile.name}' aplicado em: {target}")
    print(f"Nome de projeto aplicado: {project_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
