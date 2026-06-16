---
mode: agent
description: Migra/adapta uma query SQL de outro dialeto para HiveQL idiomático e performático.
---

Adapte para Hive (HiveQL) a query abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Dialeto de origem: ${input:origem:ex. ANSI, Oracle, SQL Server, Teradata}

Siga as instruções de Hive e a skill hive-tuning:

1. Traduza a sintaxe (paginação, funções de data/string, `QUALIFY`/`TOP`→`ROW_NUMBER` em subquery, etc.) preservando o resultado.
2. Garanta **partition pruning**: filtro literal na coluna de partição, sem função em volta.
3. Recomende formato (ORC/Parquet + compressão) e, se fizer sentido, **bucketing** para o join.
4. Aponte oportunidade de **map join** e tratamento de **skew**; alerte sobre `ORDER BY` global e small files.
5. Liste cada mudança com a consequência prática (bytes lidos, reducers) e como validar (contagens/agregados antes e depois).

Se a coluna de partição ou a granularidade não estiverem claras, pergunte antes de decidir o particionamento.
