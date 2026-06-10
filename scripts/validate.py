"""Valida a estrutura do template e o orçamento de tokens.

Checa:
- Todo profile resolve (extends/packs válidos, sem ciclo).
- Toda instruction tem front-matter com 'applyTo'.
- Toda skill (SKILL.md) tem 'name' e 'description'.
- Todo agent tem 'name' e 'description'.
- A camada always-on de cada profile cabe no orçamento de tokens.
- Nenhum arquivo de pack tem segredo óbvio ou caminho local fixo.

Saída: código 0 se ok; 1 se houver erros. Avisos não falham (use --strict).
Rode com `uv run scripts/validate.py` — o uv provisiona o Python
necessário automaticamente (metadados PEP 723 abaixo).
"""

# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
import re
from pathlib import Path

from _template_lib import (
    ALWAYS_ON_BUDGET_TOKENS,
    PACKS_DIR,
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida estrutura e orçamento de tokens do template.")
    parser.add_argument("--strict", action="store_true", help="Trata avisos como erros")
    args = parser.parse_args()

    report = Report()
    check_profiles(report)
    check_components(report)
    check_secrets(report)

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
