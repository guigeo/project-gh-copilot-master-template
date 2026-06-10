"""Scaffolder de tema: cria um pack + profile novo já no padrão do template.

Gera o conjunto que o GitHub Copilot recomenda para especializar um tema:
instrução com applyTo, skill sob-demanda, agente especialista, prompt e um
profile que estende 'common'. Tudo com front-matter correto e placeholders.

Exemplo:
    uv run scripts/new_theme.py --name dbt --globs "**/*.sql,**/*.yml" \
        --description "Projetos dbt"

Rode com `uv run` — o uv provisiona o Python necessário automaticamente
(metadados PEP 723 abaixo).
"""

# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import argparse
from pathlib import Path

from _template_lib import PACKS_DIR, PROFILES_DIR, list_packs, list_profiles

INSTRUCTION_TMPL = """---
applyTo: "{globs}"
description: Padrões de {title}. (Resuma em uma linha o que esta instrução cobre.)
---

# Instruções para {title}

## Estilo

- (Regra curta e específica de {title}.)

## Boas práticas

- (Regra curta. Mantenha conciso: detalhe pesado vai para a skill.)

## Segurança

- Não use credenciais, tokens ou caminhos locais fixos.
"""

SKILL_TMPL = """---
name: {name}-workflow
description: Use esta skill para o fluxo especializado de {title}. (Descreva quando acionar.)
---

Ao trabalhar com {title}:

1. (Passo 1.)
2. (Passo 2.)
3. (Validação / testes.)
"""

AGENT_TMPL = """---
name: {name}-reviewer
description: Revisor especializado em {title}.
tools: ["read", "search"]
infer: true
---

Você é um revisor de {title}.

Verifique:

- (Critério 1.)
- (Critério 2.)
- Ausência de segredos e caminhos locais fixos.

Separe problemas críticos de melhorias opcionais.
"""

PROMPT_TMPL = """---
mode: agent
description: Tarefa repetível para {title}.
---

(Descreva a tarefa de {title}. Peça plano antes de implementar.)

(Para receber parâmetros do usuário, use a sintaxe ${{input:nome:placeholder}};
para o código selecionado, use ${{selection}}.)
"""

PACK_META_TMPL = 'name = "{name}"\ndescription = "{description}"\n'

PROFILE_TMPL = """name = "{name}"
description = "{description}"
extends = ["common"]
packs = [{packs}]
"""


def title_from_name(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def write_if_absent(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        print(f"skip existing: {path.relative_to(PACKS_DIR.parent)}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"created: {path.relative_to(PACKS_DIR.parent)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Cria um pack + profile novo no padrão do template.")
    parser.add_argument("--name", required=True, help="Nome do tema (kebab-case), ex.: pyspark")
    parser.add_argument("--globs", default="**/*", help="applyTo da instrução, ex.: \"**/*.py\"")
    parser.add_argument("--description", default="", help="Descrição do tema")
    parser.add_argument("--on-python", action="store_true",
                        help="Profile também inclui o pack 'python'")
    parser.add_argument("--no-agent", action="store_true", help="Não gera agente")
    parser.add_argument("--no-skill", action="store_true", help="Não gera skill")
    parser.add_argument("--no-prompt", action="store_true", help="Não gera prompt")
    parser.add_argument("--no-template", action="store_true", help="Não gera scaffold de código")
    parser.add_argument("--no-profile", action="store_true", help="Não gera profile")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos existentes")
    args = parser.parse_args()

    name = args.name.strip().lower()
    title = title_from_name(name)
    description = args.description or f"Projetos de {title}."
    pack_dir = PACKS_DIR / name

    if name in list_packs() and not args.force:
        print(f"ERRO: pack '{name}' já existe. Use --force para sobrescrever arquivos.")
        return 2

    write_if_absent(pack_dir / "pack.toml",
                    PACK_META_TMPL.format(name=name, description=description), args.force)
    write_if_absent(pack_dir / "github" / "instructions" / f"{name}.instructions.md",
                    INSTRUCTION_TMPL.format(globs=args.globs, title=title), args.force)
    if not args.no_skill:
        write_if_absent(pack_dir / "github" / "skills" / f"{name}-workflow" / "SKILL.md",
                        SKILL_TMPL.format(name=name, title=title), args.force)
    if not args.no_agent:
        write_if_absent(pack_dir / "github" / "agents" / f"{name}-reviewer.agent.md",
                        AGENT_TMPL.format(name=name, title=title), args.force)
    if not args.no_prompt:
        write_if_absent(pack_dir / "github" / "prompts" / f"{name}.prompt.md",
                        PROMPT_TMPL.format(title=title), args.force)
    if not args.no_template:
        write_if_absent(pack_dir / "project" / name / "README.md",
                        f"# {title}\n\nColoque aqui os arquivos do tema {title}.\n", args.force)

    if not args.no_profile:
        packs = ['"python", ' if args.on_python else ""] + [f'"{name}"']
        packs_str = "".join(packs)
        write_if_absent(PROFILES_DIR / f"{name}.toml",
                        PROFILE_TMPL.format(name=name, description=description, packs=packs_str),
                        args.force)

    print("\nPróximos passos:")
    print(f"1. Edite os placeholders em packs/{name}/ com as regras reais.")
    print("2. Rode: uv run scripts/validate.py")
    print(f"3. Teste:  uv run scripts/new_project.py --profile {name} --target /tmp/proj-{name} --dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
