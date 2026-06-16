# GitHub Copilot Project Template

Template central para iniciar projetos já especializados em um tema (Python, SQL, SAS, Excel, ArcGIS/ArcPy, engenharia de dados…), com o **conjunto de componentes que o GitHub Copilot recomenda** — instruções, skills, agents e prompts — montado de forma **declarativa** e com **consumo inteligente de tokens** no projeto gerado.

## Ideias centrais

1. **Profiles declarativos com composição.** Um profile é um arquivo TOML que compõe *packs* (`extends` + `packs`). Criar um tema novo não exige editar Python.
2. **Capability packs.** Cada tema é uma pasta autocontida com tudo que o Copilot espera: instrução com `applyTo`, skill sob-demanda, agente especialista, prompt e scaffold de código.
3. **Token inteligente no profile, não na criação.** O que custa token em todo prompt é só a camada *always-on* (`copilot-instructions.md` + `AGENTS.md`). O resto é carregado sob-demanda. O tooling **mede e orça** isso.

## Estrutura do template

```text
profiles/          # manifestos TOML (um por profile)
packs/             # capability packs (um por tema)
  <tema>/
    pack.toml      # metadados
    github/        # vira .github/ no projeto (instructions, skills, agents, prompts, workflows)
    project/       # vira a raiz do projeto (código, README, etc.)
scripts/
  new_project.py   # cria um projeto a partir de um profile (+ relatório de tokens)
  new_theme.py     # scaffolda um pack + profile novo no padrão
  validate.py      # valida front-matter, orçamento de token e segredos
docs/              # documentação
```

## Criar um projeto

```bash
# Listar profiles
uv run scripts/new_project.py --list

# Simular (mostra plano + orçamento de tokens, sem gravar)
uv run scripts/new_project.py --profile python --target ./meu-projeto \
  --project-name "Meu Projeto" --dry-run

# Criar de fato
uv run scripts/new_project.py --profile python --target ./meu-projeto \
  --project-name "Meu Projeto"
```

Reduza o contexto inicial com flags: `--without-agents`, `--without-skills`, `--without-prompts`, `--without-ci`.

## Profiles disponíveis

| Profile | Packs | Quando usar |
|---|---|---|
| `common` | common | Base para qualquer projeto |
| `python` | common, python | Python puro, APIs, scripts |
| `python-minimal` | common, python | Python com contexto mínimo (sem agents/skills/prompts/CI) |
| `excel` | common, python, pandas, excel | Ingestão/validação/transformação de Excel (compõe pandas) |
| `sql` | common, sql | Queries, modelos analíticos, performance |
| `sas` | common, sas | Análise SAS, ETL legado, migração SAS→Python |
| `arcgis-arcpy` | common, python, arcgis-arcpy | ArcGIS Pro, ArcPy, geoprocessamento |
| `data-engineering` | common, python, sql, data-engineering | Python + SQL + docs + testes |
| `pyspark` | common, python, pyspark | Pipelines Spark, otimização de jobs, testes locais |
| `databricks` | common, python, pyspark, databricks | Lakeflow/DLT, bundles (DABs) com dev/prod, Unity Catalog |
| `web-scraping` | common, python, web-scraping | Raspagem responsável: robots.txt, rate limit, retry/backoff, parsing testável |
| `teradata` | common, sql, sql-teradata | QUALIFY, Primary/Partitioned Index, skew, COLLECT STATS, EXPLAIN |
| `sqlserver` | common, sql, sql-sqlserver | T-SQL: TOP/OFFSET, SARGable, índices, planos, parameter sniffing |
| `hive` | common, sql, sql-hive | HiveQL: partições, bucketing, ORC/Parquet, map join, vetorização |
| `oracle` | common, sql, sql-oracle | bind variables, FETCH FIRST/ROWNUM, particionamento, hints, PL/SQL |
| `pandas` | common, python, pandas | pandas moderno: Copy-on-Write, dtypes Arrow, vetorização, merge validado, pandera |

## Criar um tema novo

```bash
uv run scripts/new_theme.py --name dbt --globs "**/*.sql,**/*.yml" \
  --description "Projetos dbt"
```

Gera `packs/dbt/` (instrução, skill, agente, prompt, scaffold) e `profiles/dbt.toml` já estendendo `common`. Depois edite os placeholders e rode `validate.py`.

## Validar

```bash
uv run scripts/validate.py          # erros falham; avisos não
uv run scripts/validate.py --strict # avisos também falham
```

## Requisitos

- Apenas [uv](https://docs.astral.sh/uv/getting-started/installation/): os scripts declaram `requires-python >= 3.11` via PEP 723 e o uv baixa o Python sozinho se necessário.
- Sem uv: qualquer Python 3.11+ com `python scripts/<script>.py ...` (usa só a stdlib).

## Princípio

Não coloque tudo no contexto sempre. Camada *always-on* curta, instruções por `applyTo`, skills sob-demanda e agentes para especialidades. Ver [docs/01-estrategia-token-contexto.md](docs/01-estrategia-token-contexto.md) e [docs/05-arquitetura.md](docs/05-arquitetura.md).
