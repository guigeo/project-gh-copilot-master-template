# Manifesto da estrutura

Visão de alto nível do repositório do template. Para detalhes, ver
[docs/05-arquitetura.md](docs/05-arquitetura.md).

## Diretórios

| Caminho | Papel |
|---|---|
| `profiles/*.toml` | Manifestos declarativos (compõem packs via `extends` + `packs`) |
| `packs/<tema>/` | Capability packs: `pack.toml` + `github/` + `project/` |
| `scripts/_template_lib.py` | Resolução de profiles e contabilidade de tokens (compartilhado) |
| `scripts/new_project.py` | Cria um projeto a partir de um profile (+ relatório de tokens) |
| `scripts/new_theme.py` | Scaffolda um pack + profile novo |
| `scripts/validate.py` | Valida front-matter, orçamento de token e segredos |
| `docs/` | Documentação |
| `.github/workflows/validate.yml` | CI do template |

## Packs

| Pack | Conteúdo principal |
|---|---|
| `common` | copilot-instructions, AGENTS, PR template, docs, prompts gerais, skills gerais |
| `python` | instruções python/tests, skill de setup, agente revisor, prompt, CI + copilot-setup-steps, scaffold |
| `excel` | instrução, skill, agente, prompt, pipeline com testes e deps pandas/openpyxl (requer python) |
| `sql` | instrução, skill, agente revisor, prompt de otimização, exemplos |
| `sas` | instrução, agente, skill SAS→Python, prompt, scaffold |
| `arcgis-arcpy` | instrução, skill, agente, prompt e scaffold de ArcPy (requer python) |
| `data-engineering` | instrução, skill de qualidade de dados, agente e prompt (combina com python + sql) |
| `pyspark` | instrução Spark, skill de otimização, agente revisor, prompt e scaffold com SparkSession testável (requer python) |
| `databricks` | instrução UC/Lakeflow/serverless, skill de bundles (DABs), agente revisor, prompt e scaffold com bundle dev/prod + pipeline declarativo (requer python e pyspark) |

## Profiles

`common`, `python`, `python-minimal`, `excel`, `sql`, `sas`, `arcgis-arcpy`, `data-engineering`, `pyspark`, `databricks`.
Listar em runtime: `python scripts/new_project.py --list`.
