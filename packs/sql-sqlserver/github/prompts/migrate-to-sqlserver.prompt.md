---
mode: agent
description: Migra/adapta uma query SQL de outro dialeto para T-SQL (SQL Server) idiomático e performático.
---

Adapte para SQL Server (T-SQL) a query abaixo (ou o arquivo aberto, se não houver seleção):

${selection}

Dialeto de origem: ${input:origem:ex. ANSI, Oracle, Teradata, Hive}

Siga as instruções de SQL Server e a skill sqlserver-tuning:

1. Traduza a sintaxe (paginação → `OFFSET/FETCH`, `NVL`→`ISNULL`/`COALESCE`, `ROWNUM`→`ROW_NUMBER`/`TOP`, datas/strings) preservando o resultado.
2. Garanta predicados SARGable: troque funções sobre colunas filtradas por intervalos; elimine conversão implícita.
3. Sugira índices (clustered/nonclustered com `INCLUDE`) para o padrão de acesso.
4. Aponte risco de parameter sniffing e UDF escalar, com a alternativa.
5. Liste cada mudança com a consequência prática e como validar (contagens/agregados e `SET STATISTICS IO`).

Se a granularidade ou as chaves não estiverem claras, pergunte antes de alterar.
