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
- **Dependências Python**: só o pack `python` traz `project/pyproject.toml` (base, com as
  sentinelas `# __PACK_DEPENDENCIES__` e `# __PACK_DEPENDENCY_GROUPS__`). Um pack que precisa
  de bibliotecas declara só os extras em `pack.toml`:

  ```toml
  [python]
  dependencies = ["pandas>=2.2.0"]
  [python.dependency-groups]   # opcional (grupos como dynamic)
  dynamic = ["playwright>=1.47.0"]
  ```

  O `new_project` compõe um único pyproject a partir do base + os extras dos packs do profile
  (ordem base→tema, sem duplicatas). Não recrie `pyproject.toml` em outros packs.
- Não introduza segredos nem caminhos locais fixos.
- Rode `python scripts/validate.py` antes de concluir qualquer alteração. Ele também **gera cada
  profile Python e roda `ruff check`/`ruff format`** no projeto — o scaffold tem de passar no
  próprio CI. (Pule esse passo com `--no-lint` só em debug. O lint exige `ruff`; instale com
  `pip install ruff`.)

## Comandos

Os scripts do template exigem **apenas Python 3.11+** (usam só a biblioteca padrão).
Use `python` (ou `python3`) direto — sem uv.

```bash
python scripts/validate.py
python scripts/new_project.py --list
python scripts/new_project.py --profile <nome> --target <dir> --dry-run

# Ou abra o assistente interativo:
./novo-projeto.sh          # Windows: novo-projeto.cmd
```
