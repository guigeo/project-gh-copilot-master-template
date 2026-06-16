---
mode: agent
description: Migra/adapta uma query SQL de outro dialeto para Teradata idiomático e performático.
---

Adapte para Teradata a query SQL abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Dialeto de origem: ${input:origem:ex. ANSI, Oracle, SQL Server, Hive}

Siga as instruções de Teradata e a skill teradata-tuning:

1. Traduza a sintaxe (paginação → `QUALIFY`/`TOP`, funções de data/string, `NVL`→`COALESCE`, etc.) preservando o resultado.
2. Defina o **Primary Index** adequado para distribuição e join; aponte risco de skew.
3. Indique onde declarar **PPI** e quais `COLLECT STATISTICS` rodar.
4. Reescreva "última linha por chave" com `QUALIFY ROW_NUMBER()` quando aplicável.
5. Liste cada mudança com a consequência prática e como validar a equivalência (contagens/agregados antes e depois).

Se a granularidade, as chaves ou a coluna de distribuição não estiverem claras, pergunte antes de decidir o PI.
