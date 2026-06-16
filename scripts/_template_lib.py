"""Funções compartilhadas: resolução de profiles/packs e contabilidade de tokens.

Usado por new_project.py, new_theme.py e validate.py.

Conceito central de token:
- "always-on": entra no contexto do Copilot em TODO prompt (copilot-instructions + AGENTS).
- "sob-demanda": carregado só quando acionado (instructions por applyTo, skills, prompts, agents).
- "projeto": código/config que NÃO entra no contexto do Copilot (templates, CI, PR template).
"""

from __future__ import annotations

import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    sys.exit(
        f"Este script precisa de Python 3.11+ (você está no {sys.version.split()[0]}).\n"
        "Rode com uv, que baixa o Python certo sozinho:\n"
        "    uv run scripts/<script>.py ...\n"
        "Instalar uv: https://docs.astral.sh/uv/getting-started/installation/"
    )

from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT / "profiles"
PACKS_DIR = ROOT / "packs"

# Pack cuja presença dispara a nomeação de pacote Python no projeto gerado.
PYTHON_PACK = "python"

# Orçamento (tokens) da camada sempre carregada. Acima disso, avisa.
ALWAYS_ON_BUDGET_TOKENS = 1500

# Categorias que podem ser excluídas via flags --without-* ou exclude_categories.
EXCLUDABLE_CATEGORIES = {"agents", "skills", "prompts", "ci", "instructions"}

# Categorias que contam como contexto do Copilot (para relatório de token).
CONTEXT_CATEGORIES = {"always-on", "instructions", "skills", "prompts", "agents"}


class TemplateError(Exception):
    """Erro de configuração do template (profile/pack inválido)."""


@dataclass
class ResolvedProfile:
    name: str
    description: str
    packs: list[str]
    exclude_categories: set[str] = field(default_factory=set)


def _read_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def list_profiles() -> list[str]:
    return sorted(p.stem for p in PROFILES_DIR.glob("*.toml"))


def list_packs() -> list[str]:
    return sorted(p.name for p in PACKS_DIR.iterdir() if p.is_dir())


def pack_description(name: str) -> str:
    meta = PACKS_DIR / name / "pack.toml"
    if meta.exists():
        return _read_toml(meta).get("description", "")
    return ""


def resolve_profile(name: str) -> ResolvedProfile:
    """Resolve extends/packs em uma lista ordenada de packs (base → tema)."""
    path = PROFILES_DIR / f"{name}.toml"
    if not path.exists():
        raise TemplateError(
            f"Profile '{name}' não encontrado. Disponíveis: {', '.join(list_profiles())}"
        )

    visiting: set[str] = set()

    def _resolve(profile_name: str) -> tuple[list[str], set[str]]:
        if profile_name in visiting:
            raise TemplateError(f"Ciclo de 'extends' detectado em '{profile_name}'")
        visiting.add(profile_name)

        ppath = PROFILES_DIR / f"{profile_name}.toml"
        if not ppath.exists():
            raise TemplateError(f"Profile '{profile_name}' (referenciado em extends) não existe")
        data = _read_toml(ppath)

        packs: list[str] = []
        excludes: set[str] = set()
        for parent in data.get("extends", []):
            parent_packs, parent_excludes = _resolve(parent)
            packs.extend(parent_packs)
            excludes |= parent_excludes
        packs.extend(data.get("packs", []))
        excludes |= set(data.get("exclude_categories", []))

        visiting.discard(profile_name)
        return packs, excludes

    packs, excludes = _resolve(name)

    # Dedupe preservando a primeira ocorrência (base vem antes do tema).
    seen: set[str] = set()
    ordered: list[str] = []
    for pack in packs:
        if pack in seen:
            continue
        if not (PACKS_DIR / pack).is_dir():
            raise TemplateError(f"Pack '{pack}' (usado por '{name}') não existe em packs/")
        seen.add(pack)
        ordered.append(pack)

    data = _read_toml(path)
    return ResolvedProfile(
        name=name,
        description=data.get("description", ""),
        packs=ordered,
        exclude_categories=excludes,
    )


def classify(dest_rel: str) -> str:
    """Classifica um arquivo pelo caminho de destino (relativo à raiz do projeto)."""
    p = dest_rel.replace("\\", "/")
    if p == ".github/copilot-instructions.md" or p == "AGENTS.md":
        return "always-on"
    if p.startswith(".github/instructions/"):
        return "instructions"
    if p.startswith(".github/skills/"):
        return "skills"
    if p.startswith(".github/agents/"):
        return "agents"
    if p.startswith(".github/prompts/"):
        return "prompts"
    if p.startswith(".github/workflows/"):
        return "ci"
    return "project"


def iter_pack_files(pack: str) -> list[tuple[Path, str, str]]:
    """Lista (arquivo_origem, destino_relativo, categoria) de um pack.

    - packs/<pack>/github/**  -> .github/**
    - packs/<pack>/project/** -> ** (raiz do projeto)
    """
    base = PACKS_DIR / pack
    results: list[tuple[Path, str, str]] = []
    for source_root, prefix in (("github", ".github"), ("project", "")):
        root = base / source_root
        if not root.is_dir():
            continue
        for child in sorted(root.rglob("*")):
            if child.is_dir():
                continue
            rel = child.relative_to(root).as_posix()
            dest_rel = f"{prefix}/{rel}" if prefix else rel
            dest_rel = dest_rel.lstrip("/")
            results.append((child, dest_rel, classify(dest_rel)))
    return results


def build_file_map(
    profile: ResolvedProfile, extra_excludes: set[str] | None = None
) -> dict[str, tuple[Path, str]]:
    """Mapa destino_relativo -> (arquivo_origem, categoria).

    Packs posteriores (tema) sobrescrevem anteriores (base) em colisão de destino.
    """
    excludes = set(profile.exclude_categories) | (extra_excludes or set())
    file_map: dict[str, tuple[Path, str]] = {}
    for pack in profile.packs:
        for src, dest_rel, category in iter_pack_files(pack):
            if category in excludes:
                continue
            file_map[dest_rel] = (src, category)
    if not file_map:
        raise TemplateError("Nenhum arquivo restou após aplicar os filtros de categoria")
    return file_map


def estimate_tokens(text: str) -> int:
    """Heurística simples: ~4 caracteres por token."""
    return max(1, len(text) // 4)


def estimate_tokens_for_file(path: Path) -> int:
    try:
        return estimate_tokens(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, OSError):
        return max(1, path.stat().st_size // 4)


# Sentinelas no pyproject base (packs/python/project/pyproject.toml) que o
# new_project substitui pelas dependências compostas dos packs do profile.
DEP_SENTINEL = "# __PACK_DEPENDENCIES__"
GROUP_SENTINEL = "# __PACK_DEPENDENCY_GROUPS__"


def collect_python_requirements(
    profile: ResolvedProfile,
) -> tuple[list[str], dict[str, list[str]]]:
    """Junta as dependências declaradas em `[python]` de cada pack do profile.

    Cada pack declara só seus extras em `pack.toml`:

        [python]
        dependencies = ["pandas>=2.2.0"]
        [python.dependency-groups]
        dynamic = ["playwright>=1.47.0"]

    Retorna (dependencies, dependency_groups), na ordem dos packs (base -> tema)
    e sem duplicatas, preservando a primeira ocorrência.
    """
    deps: list[str] = []
    seen: set[str] = set()
    groups: dict[str, list[str]] = {}

    for pack in profile.packs:
        meta = PACKS_DIR / pack / "pack.toml"
        if not meta.exists():
            continue
        python_cfg = _read_toml(meta).get("python", {})
        for dep in python_cfg.get("dependencies", []):
            if dep not in seen:
                seen.add(dep)
                deps.append(dep)
        for group, items in python_cfg.get("dependency-groups", {}).items():
            bucket = groups.setdefault(group, [])
            for item in items:
                if item not in bucket:
                    bucket.append(item)

    return deps, groups


def render_pyproject(base_text: str, deps: list[str], groups: dict[str, list[str]]) -> str:
    """Substitui as sentinelas do pyproject base pelas deps/grupos compostos.

    Mantém o restante do arquivo (ruff, build-system, pytest) intacto.
    """
    lines: list[str] = []
    for line in base_text.splitlines():
        stripped = line.strip()
        if stripped == DEP_SENTINEL:
            lines.extend(f'    "{dep}",' for dep in deps)
            continue
        if stripped == GROUP_SENTINEL:
            for group, items in groups.items():
                lines.append(f"{group} = [")
                lines.extend(f'    "{item}",' for item in items)
                lines.append("]")
            continue
        lines.append(line)
    return "\n".join(lines) + "\n"


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)
