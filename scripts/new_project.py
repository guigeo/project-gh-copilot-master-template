"""Cria um novo projeto a partir de um profile do template.

Resolve o profile (extends + packs), copia os arquivos para o destino e,
em projetos Python, aplica o nome do pacote. Com --dry-run, mostra a
contabilidade de tokens separando contexto sempre-carregado, sob-demanda
e arquivos de projeto.

Rode com `uv run scripts/new_project.py ...` — o uv provisiona o Python
necessário automaticamente (metadados PEP 723 abaixo).
"""

# /// script
# requires-python = ">=3.11"
# ///

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
    EXCLUDABLE_CATEGORIES,
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

TEMPLATE_VERSION = "2.0"

CATEGORY_ORDER = [
    "always-on",
    "instructions",
    "skills",
    "prompts",
    "agents",
    "ci",
    "project",
]

CATEGORY_LABEL = {
    "always-on": "Sempre carregado (always-on)",
    "instructions": "Instruções por applyTo (sob-demanda)",
    "skills": "Skills (sob-demanda)",
    "prompts": "Prompts (sob-demanda)",
    "agents": "Agents (sob-demanda)",
    "ci": "CI / workflows (fora do contexto)",
    "project": "Arquivos de projeto (fora do contexto)",
}


def flags_to_excludes(args: argparse.Namespace) -> set[str]:
    excludes: set[str] = set()
    if args.without_agents:
        excludes.add("agents")
    if args.without_skills:
        excludes.add("skills")
    if args.without_prompts:
        excludes.add("prompts")
    if args.without_ci:
        excludes.add("ci")
    return excludes


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
    profile: ResolvedProfile, file_map: dict[str, tuple[Path, str]], target: Path, project_name: str
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

    print("\nDRY RUN — nenhum arquivo foi copiado")
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


def apply_python_project_naming(target: Path, project_name: str, force: bool) -> None:
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
    replace_token_in_text_files(target, "nome_pacote", project_name)
    replace_in_file(target / "pyproject.toml", 'name = "nome-projeto"', f'name = "{project_name}"')


def write_project_manifest(target: Path, profile: ResolvedProfile, project_name: str) -> None:
    manifest = {
        "template_version": TEMPLATE_VERSION,
        "profile": profile.name,
        "packs": profile.packs,
        "project_name": project_name,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    path = target / ".copilot-template.json"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote: .copilot-template.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cria um projeto a partir de um profile do template.")
    parser.add_argument("--profile", help="Profile a aplicar (ver --list)")
    parser.add_argument("--target", help="Diretório destino do projeto")
    parser.add_argument("--project-name", help="Nome do projeto (normalizado para snake_case)")
    parser.add_argument("--without-agents", action="store_true")
    parser.add_argument("--without-skills", action="store_true")
    parser.add_argument("--without-prompts", action="store_true")
    parser.add_argument("--without-ci", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Mostra plano + tokens, sem gravar")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos existentes")
    parser.add_argument("--list", action="store_true", help="Lista profiles disponíveis e sai")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.list:
        print("Profiles disponíveis:")
        for name in list_profiles():
            try:
                prof = resolve_profile(name)
                print(f"- {name}: {prof.description}  [packs: {', '.join(prof.packs)}]")
            except TemplateError as exc:
                print(f"- {name}: (erro) {exc}")
        return 0

    if not args.profile or not args.target:
        build_parser().error("--profile e --target são obrigatórios (ou use --list)")

    try:
        profile = resolve_profile(args.profile)
        file_map = build_file_map(profile, flags_to_excludes(args))
    except TemplateError as exc:
        print(f"ERRO: {exc}")
        return 2

    target = Path(args.target).resolve()
    project_name = normalize_project_name(args.project_name or target.name)

    if args.dry_run:
        print_token_report(profile, file_map, target, project_name)
        return 0

    target.mkdir(parents=True, exist_ok=True)
    copy_files(file_map, target, args.force)

    if PYTHON_PACK in profile.packs:
        compose_pyproject(target, profile)
        apply_python_project_naming(target, project_name, args.force)

    write_project_manifest(target, profile, project_name)

    print(f"\nProfile '{profile.name}' aplicado em: {target}")
    print(f"Nome de projeto aplicado: {project_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
