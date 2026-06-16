# Oracle (SQL + PL/SQL)

Convenções específicas de Oracle (complementam o pack `sql`).

- Use bind variables (`:param`), nunca literais concatenados (hard parse + injeção).
- Top-N com `FETCH FIRST n ROWS ONLY`; cuidado com `ROWNUM` antes do `ORDER BY`.
- Mantenha predicados SARGable; conversões explícitas (`TO_DATE`/`TO_NUMBER`).
- Particione tabelas grandes e filtre a chave de partição (pruning); índice local vs global conforme o acesso.
- Mantenha estatísticas com `DBMS_STATS`; hints só como último recurso.
- Em PL/SQL, use `BULK COLLECT` + `FORALL` em vez de linha a linha.

Veja `exemplo_topn.sql` para o padrão idiomático.
