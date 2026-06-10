---
name: databricks-bundles
description: Use esta skill para criar, alterar ou depurar Declarative Automation Bundles (DABs) — databricks.yml, resources, targets dev/prod e deploy.
---

Ao trabalhar com bundles (DABs):

1. **Estrutura**: `databricks.yml` define `bundle.name` e `targets`; cada recurso (job, pipeline) vive em `resources/*.yml` incluído via `include`.
2. **Targets**: `dev` com `mode: development` (prefixa recursos com o usuário e pausa schedules/triggers — seguro para iterar); `prod` com `mode: production` e, idealmente, `run_as` com service principal.
3. **Parametrização**: o que muda entre ambientes (catálogo, schema, host) vai em `variables` ou interpolação (`${bundle.target}`, `${workspace.current_user...}`); nunca duplique o yaml do recurso por ambiente.
4. **Caminhos**: paths em `resources/*.yml` são relativos ao próprio arquivo (ex.: `../src/...`).
5. **Ciclo**: `databricks bundle validate` → `deploy -t dev` → `run -t dev <recurso>`; só depois `deploy -t prod`.
6. **CI/CD**: PR roda `validate`; merge na main faz `deploy -t prod`. Nenhum deploy manual em prod.
7. **Depuração**: erro de schema do yaml → `validate` aponta o campo; recurso não aparece → confira o `include` e o nome do target; estado inconsistente → `databricks bundle summary -t <target>`.

Nunca edite pela UI um recurso gerenciado pelo bundle: o próximo deploy sobrescreve a mudança.
