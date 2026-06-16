---
mode: agent
description: Migra/adapta uma query SQL de outro dialeto para Oracle idiomático e performático.
---

Adapte para Oracle a query abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Dialeto de origem: ${input:origem:ex. ANSI, SQL Server, Teradata, Hive}

Siga as instruções de Oracle e a skill oracle-tuning:

1. Traduza a sintaxe (`TOP`/`LIMIT`→`FETCH FIRST`, `ISNULL`→`NVL`/`COALESCE`, `QUALIFY`→`ROW_NUMBER` em subquery, datas com `TO_DATE`) preservando o resultado.
2. Use **bind variables** no lugar de literais concatenados; aponte risco de hard parse.
3. Garanta SARGability (sem função/conversão implícita em coluna indexada) e indique índices/partition pruning úteis.
4. Se houver lógica procedural, mostre o padrão `BULK COLLECT` + `FORALL` em vez de linha a linha.
5. Liste cada mudança com a consequência prática e como validar (contagens/agregados e plano via `DBMS_XPLAN`).

Se a granularidade, as chaves ou a chave de partição não estiverem claras, pergunte antes de alterar.
