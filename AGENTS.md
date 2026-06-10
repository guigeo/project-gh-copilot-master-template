# AGENTS.md (repositório do template)

Este arquivo orienta agentes de codificação que trabalham **neste repositório do template**.
(Não confundir com o `AGENTS.md` que o template entrega aos projetos gerados, que vive em
`packs/common/project/AGENTS.md`.)

## Contexto

Repositório que gera projetos especializados de GitHub Copilot a partir de **profiles**
(manifestos TOML em `profiles/`) que compõem **packs** (`packs/<tema>/`).

## Conceitos

- **Profile** (`profiles/<nome>.toml`): `extends` (outros profiles) + `packs` + `exclude_categories`.
- **Pack** (`packs/<tema>/`): `pack.toml` + `github/` (vira `.github/`) + `project/` (vira raiz do projeto).
- **Always-on**: só `.github/copilot-instructions.md` e `AGENTS.md` entram no contexto a cada prompt.
  Mantenha-os curtos (orçamento em `scripts/_template_lib.py`).

## Regras para agentes

- Lógica de resolução e contabilidade de token mora em `scripts/_template_lib.py`. Reuse, não duplique.
- Ao criar um tema, prefira `scripts/new_theme.py` a montar arquivos na mão.
- Instruções devem ter `applyTo`; skills e agents devem ter `name` + `description`.
- Detalhe pesado vai para skills, não para instructions nem para a camada always-on.
- Não introduza segredos nem caminhos locais fixos.
- Rode `uv run scripts/validate.py` antes de concluir qualquer alteração.

## Comandos

Sempre use `uv run` (não `python` direto): os scripts exigem Python 3.11+
e o uv provisiona a versão certa automaticamente (PEP 723).

```bash
uv run scripts/validate.py
uv run scripts/new_project.py --list
uv run scripts/new_project.py --profile <nome> --target <dir> --dry-run
```
