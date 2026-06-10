---
mode: agent
description: Adiciona um recurso (job ou pipeline) ao bundle Databricks do projeto.
---

Adicione um recurso ao bundle deste projeto.

Recurso desejado: ${input:recurso:ex. job diário que roda src/pacote/main.py, pipeline Lakeflow para tabela X}

Siga a skill databricks-bundles:

1. Leia o `databricks.yml` e os `resources/*.yml` existentes para seguir as convenções do projeto (nomes, variables, targets).
2. Crie o yaml em `resources/`, parametrizado por target (nada de valor fixo de dev/prod no recurso).
3. Prefira serverless; declare schedule/trigger pausável em dev (`mode: development` já cuida disso).
4. Se o recurso aponta para código novo, crie o módulo em `src/` seguindo as instruções de PySpark do projeto.
5. Informe os comandos para testar: `databricks bundle validate` e `databricks bundle run -t dev <recurso>`.
