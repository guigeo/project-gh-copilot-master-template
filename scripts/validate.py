"""Valida a estrutura do template e o orçamento de tokens.

Checa:
- Todo profile resolve (extends/packs válidos, sem ciclo).
- Toda instruction tem front-matter com 'applyTo'.
- Toda skill (SKILL.md) tem 'name' e 'description'.
- Todo agent tem 'name' e 'description'.
- A camada always-on de cada profile cabe no orçamento de tokens.
- Nenhum arquivo de pack tem segredo óbvio ou caminho local fixo.
- Cada profile Python gera um projeto que passa em `ruff check`/`ruff format`
  (o mesmo lint do CI entregue ao projeto). Pulado se o ruff não estiver
  instalado (`pip install ruff`).

Requer apenas Python 3.11+ (usa só a biblioteca padrão; o ruff é opcional).
Saída: código 0 se ok; 1 se houver erros. Avisos não falham (use --strict).
Rode com: python scripts/validate.py
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from _template_lib import (
    ALWAYS_ON_BUDGET_TOKENS,
    PACKS_DIR,
    PYTHON_PACK,
    TemplateError,
    build_file_map,
    estimate_tokens_for_file,
    list_packs,
    list_profiles,
    resolve_profile,
)

SECRET_PATTERNS = [
    (re.compile(r"(?i)(password|senha|secret|api[_-]?key|token)\s*[:=]\s*[\"']?[A-Za-z0-9/+_-]{6,}"),
     "possível credencial hardcoded"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "possível AWS access key"),
    (re.compile(r"(?i)/Users/[a-z0-9._-]+/"), "caminho local fixo (/Users/...)"),
    (re.compile(r"[A-Za-z]:\\\\Users\\\\"), "caminho local fixo (C:\\Users\\...)"),
]

# Placeholders legítimos que NÃO devem disparar o alarme de segredo.
SECRET_ALLOWLIST = re.compile(r"(?i)(example|exemplo|sua[_-]?senha|seu[_-]?token|xxx|<.*>|\.\.\.)")


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return None  # sem fechamento '---'


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def check_profiles(report: Report) -> None:
    for name in list_profiles():
        try:
            profile = resolve_profile(name)
            build_file_map(profile)
        except TemplateError as exc:
            report.error(f"profile '{name}': {exc}")
            continue

        always_on = sum(
            estimate_tokens_for_file(src)
            for src, category in build_file_map(profile).values()
            if category == "always-on"
        )
        if always_on > ALWAYS_ON_BUDGET_TOKENS:
            report.error(
                f"profile '{name}': camada always-on ~{always_on} tokens "
                f"> orçamento {ALWAYS_ON_BUDGET_TOKENS}"
            )


def rel(path: Path) -> str:
    return path.relative_to(PACKS_DIR.parent).as_posix()


def check_components(report: Report) -> None:
    for pack in list_packs():
        base = PACKS_DIR / pack / "github"
        if not base.is_dir():
            continue

        for inst in (base / "instructions").glob("*.instructions.md"):
            fm = parse_front_matter(inst.read_text(encoding="utf-8"))
            if fm is None:
                report.error(f"{rel(inst)}: sem front-matter válido")
            else:
                if "applyTo" not in fm:
                    report.error(f"{rel(inst)}: instruction sem 'applyTo'")
                if "description" not in fm:
                    report.warn(f"{rel(inst)}: instruction sem 'description' (recomendado)")

        for skill in (base / "skills").glob("*/SKILL.md"):
            fm = parse_front_matter(skill.read_text(encoding="utf-8"))
            if fm is None:
                report.error(f"{rel(skill)}: sem front-matter válido")
            else:
                for field in ("name", "description"):
                    if field not in fm:
                        report.error(f"{rel(skill)}: skill sem '{field}'")

        for agent in (base / "agents").glob("*.agent.md"):
            fm = parse_front_matter(agent.read_text(encoding="utf-8"))
            if fm is None:
                report.error(f"{rel(agent)}: sem front-matter válido")
            else:
                for field in ("name", "description"):
                    if field not in fm:
                        report.error(f"{rel(agent)}: agent sem '{field}'")
                if "tools" not in fm:
                    report.warn(f"{rel(agent)}: agent sem 'tools' (recomendado)")

        for prompt in (base / "prompts").glob("*.prompt.md"):
            text = prompt.read_text(encoding="utf-8")
            fm = parse_front_matter(text)
            if fm is None:
                report.error(f"{rel(prompt)}: sem front-matter válido")
            elif "description" not in fm:
                report.error(f"{rel(prompt)}: prompt sem 'description'")
            if "{{" in text:
                report.warn(
                    f"{rel(prompt)}: placeholder '{{{{...}}}}' não é interpolado; "
                    "use ${input:nome} ou ${selection}"
                )


def check_secrets(report: Report) -> None:
    for path in PACKS_DIR.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line in text.splitlines():
            if SECRET_ALLOWLIST.search(line):
                continue
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(line):
                    report.warn(f"{rel(path)}: {label} -> {line.strip()[:80]}")


def _python_profiles() -> list[str]:
    """Profiles cujos packs incluem o pack python (geram um pyproject)."""
    nomes: list[str] = []
    for name in list_profiles():
        try:
            if PYTHON_PACK in resolve_profile(name).packs:
                nomes.append(name)
        except TemplateError:
            continue
    return nomes


def check_scaffold_lint(report: Report) -> None:
    """Gera cada profile Python e roda o mesmo lint do CI (ruff) no projeto.

    Linta o artefato gerado — não o scaffold cru — porque a classificação de
    imports do ruff depende do nome do pacote do projeto; só o projeto final
    reflete o que o CI entregue ao usuário vai checar.
    """
    if shutil.which("ruff") is None:
        report.warn("ruff indisponível; lint dos scaffolds pulado (instale com `pip install ruff`)")
        return

    new_project = Path(__file__).resolve().parent / "new_project.py"
    for name in _python_profiles():
        with tempfile.TemporaryDirectory() as tmp:
            # Gera a variante COMPLETA (pyproject + testes + exemplos): é a que
            # tem código Python real para o ruff checar. O default é cru (src/ vazio).
            gen = subprocess.run(
                [sys.executable, str(new_project), "--profile", name,
                 "--target", tmp, "--project-name", "lint check", "--force",
                 "--with-pyproject", "--with-tests", "--with-examples"],
                capture_output=True, text=True,
            )
            if gen.returncode != 0:
                report.error(f"lint '{name}': falha ao gerar projeto -> {gen.stderr.strip()[:200]}")
                continue
            # cwd no projeto gerado: o ruff detecta a raiz/first-party pelo cwd,
            # exatamente como o CI (`ruff check .` na raiz do projeto).
            check = subprocess.run(["ruff", "check", "."], cwd=tmp, capture_output=True, text=True)
            if check.returncode != 0:
                report.error(f"profile '{name}': scaffold falha em 'ruff check'\n{check.stdout.strip()}")
            fmt = subprocess.run(
                ["ruff", "format", "--check", "."], cwd=tmp, capture_output=True, text=True
            )
            if fmt.returncode != 0:
                detalhe = (fmt.stdout or fmt.stderr).strip()
                report.error(f"profile '{name}': scaffold falha em 'ruff format --check'\n{detalhe}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida estrutura e orçamento de tokens do template.")
    parser.add_argument("--strict", action="store_true", help="Trata avisos como erros")
    parser.add_argument("--no-lint", action="store_true",
                        help="Pula o lint (ruff) dos projetos gerados")
    args = parser.parse_args()

    report = Report()
    check_profiles(report)
    check_components(report)
    check_secrets(report)
    if not args.no_lint:
        check_scaffold_lint(report)

    for warn in report.warnings:
        print(f"AVISO: {warn}")
    for err in report.errors:
        print(f"ERRO:  {err}")

    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    if failed:
        print(f"\nFALHOU: {len(report.errors)} erro(s), {len(report.warnings)} aviso(s).")
        return 1

    print(f"\nOK: estrutura válida. {len(report.warnings)} aviso(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
