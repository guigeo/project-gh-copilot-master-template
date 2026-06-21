# Criando profiles e temas

Há dois níveis: **profile** (combina temas existentes) e **tema/pack** (uma especialização nova).

## Caso 1 — Novo profile combinando packs existentes

Crie um arquivo em `profiles/`:

```toml
# profiles/api-sql.toml
name = "api-sql"
description = "API Python com acesso a SQL."
extends = ["common"]
packs = ["python", "sql"]
```

Pronto. Valide e teste:

```bash
python scripts/validate.py
python scripts/new_project.py --profile api-sql --target /tmp/api-sql --dry-run
```

Campos do manifesto:

- `extends`: lista de outros profiles cujos packs são herdados.
- `packs`: packs próprios, aplicados após os herdados (tema sobrescreve base em colisão).
- `exclude_categories`: remove categorias inteiras (`agents`, `skills`, `prompts`, `ci`, `instructions`).

## Caso 2 — Novo tema (capability pack)

Use o scaffolder, que já cria o conjunto recomendado pelo Copilot com front-matter correto:

```bash
python scripts/new_theme.py --name databricks --globs "**/*.py" \
  --description "Projetos Databricks" --on-python
```

Isso gera:

```text
packs/databricks/
  pack.toml
  github/instructions/databricks.instructions.md   # applyTo já preenchido
  github/skills/databricks-workflow/SKILL.md
  github/agents/databricks-reviewer.agent.md
  github/prompts/databricks.prompt.md
  project/databricks/README.md
profiles/databricks.toml                            # extends common (+ python com --on-python)
```

Flags úteis: `--no-agent`, `--no-skill`, `--no-prompt`, `--no-template`, `--no-profile`, `--force`.

Depois:

1. Edite os placeholders em `packs/databricks/` com as regras reais.
2. Mantenha a instrução curta; mova detalhe para a skill.
3. `python scripts/validate.py`
4. `python scripts/new_project.py --profile databricks --target /tmp/x --dry-run`

## Regras de qualidade

- Instrução: sempre com `applyTo` específico.
- Skill/agent: sempre com `name` + `description`.
- Não estourar o orçamento da camada always-on (o `validate.py` falha se estourar).
- Sem segredos nem caminhos locais fixos (o `validate.py` avisa).

## O que o `new_project.py` faz e não faz

Faz: resolve o profile, copia arquivos, renomeia o pacote Python e grava `.copilot-template.json`.
Não faz: instalar dependências, criar venv ou rodar testes — isso fica a cargo do projeto gerado (`pytest` e o gerenciador que ele adotar).
