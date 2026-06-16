# SQL Server (T-SQL)

Convenções específicas de SQL Server (complementam o pack `sql`).

- Mantenha predicados **SARGable**: sem função/conversão implícita sobre coluna indexada no filtro.
- Pagine com `OFFSET/FETCH` (+ `ORDER BY`); use funções de janela em vez de subqueries correlacionadas.
- Use índice de cobertura (`INCLUDE`) para eliminar Key Lookup.
- Evite UDF escalar em `WHERE`/`SELECT`; CTE reusada N vezes vira `#temp`.
- Prefira RCSI a `WITH (NOLOCK)`; cuide de parameter sniffing com `OPTION (RECOMPILE)`.

Veja `exemplo_paginacao.sql` para o padrão idiomático.
