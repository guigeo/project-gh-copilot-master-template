# Teradata

Convenções específicas de Teradata (complementam o pack `sql`).

- Defina o **Primary Index** pensando em distribuição uniforme e nas chaves de join.
- Para tabelas grandes com filtro de data, use **PPI** e filtre sempre a coluna de partição.
- Rode `COLLECT STATISTICS` no PI, colunas de join e de filtro.
- Prefira `QUALIFY ROW_NUMBER()` a subqueries para "última linha por chave".
- Intermediários reutilizados: tabelas **VOLATILE** com PI adequado.
- Antes de escalar, leia o `EXPLAIN` e elimine product joins e skew.

Veja `exemplo_qualify.sql` para o padrão idiomático.
