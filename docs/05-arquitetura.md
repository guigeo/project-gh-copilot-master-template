# Arquitetura: profiles, packs e tokens

## Visão geral

```text
profiles/<nome>.toml   →   compõe   →   packs/<tema>/   →   copiado para   →   projeto novo
```

- Um **profile** descreve *o que* um projeto recebe, sem repetir arquivos.
- Um **pack** agrupa *todos* os componentes de um tema.
- O **script** resolve o profile e copia só o necessário, medindo o custo de token.

## Profile (manifesto declarativo)

`profiles/python.toml`:

```toml
name = "python"
description = "Projeto Python puro."
extends = ["common"]      # herda os packs de outro profile
packs = ["python"]        # adiciona packs próprios
# exclude_categories = ["agents", "skills"]   # opcional
```

Resolução:

1. `extends` é resolvido recursivamente (detecta ciclos).
2. Os packs viram uma lista ordenada **base → tema** (dedupe preservando a primeira posição).
3. Em colisão de arquivo, o pack **posterior** (tema) sobrescreve o anterior (base).
4. `exclude_categories` e flags `--without-*` removem categorias inteiras.

## Pack (capability pack)

```text
packs/<tema>/
  pack.toml                       # name + description
  github/
    instructions/<tema>.instructions.md   # applyTo: regras curtas
    skills/<skill>/SKILL.md                # workflow pesado, sob-demanda
    agents/<tema>-reviewer.agent.md        # especialista
    prompts/<tema>.prompt.md               # tarefa repetível
    workflows/*.yml                        # CI (opcional)
  project/                        # vira a raiz do projeto (scaffold de código)
```

- `github/**` → `.github/**` no projeto.
- `project/**` → raiz do projeto.

## Categorias e tokens

Cada arquivo é classificado pelo destino:

| Categoria | Entra no contexto a cada prompt? | Exemplos |
|---|---|---|
| `always-on` | **Sim** | `.github/copilot-instructions.md`, `AGENTS.md` |
| `instructions` | Só quando o arquivo casa com `applyTo` | `python.instructions.md` |
| `skills` | Só quando a skill é acionada | `SKILL.md` |
| `prompts` | Só quando o prompt é chamado | `*.prompt.md` |
| `agents` | Só quando o agente é selecionado | `*.agent.md` |
| `project` / `ci` | **Não** (não é contexto do Copilot) | `pyproject.toml`, workflows |

O `--dry-run` e o `validate.py` somam tokens (~4 caracteres/token) e tratam a camada
`always-on` com um **orçamento** (`ALWAYS_ON_BUDGET_TOKENS` em `scripts/_template_lib.py`).
Acima do orçamento, o tooling avisa — porque é esse número que pesa em *todo* prompt.

## Por que isso consome menos token no projeto

- A base sempre-carregada é pequena e fixa.
- Regras específicas só aparecem quando se mexe no arquivo daquele tema (`applyTo`).
- O conhecimento profundo fica em skills, carregadas só sob demanda.
- Nada de documentação externa inteira colada nas instruções.

## Manifesto no projeto gerado

Cada projeto recebe um `.copilot-template.json` registrando profile, packs e versão.
Ele **não** entra no contexto do Copilot; serve para rastrear a origem e permitir re-sync futuro.
