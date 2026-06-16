# Hive (HiveQL)

Convenções específicas de Hive (complementam o pack `sql`).

- Particione por coluna de baixa cardinalidade usada em filtro; sempre filtre a partição com literal.
- Use ORC/Parquet + compressão; evite TEXTFILE e o problema de small files.
- Deixe o map join atuar com tabela pequena; trate skew quando houver.
- Mantenha vetorização ligada e rode `ANALYZE TABLE ... COMPUTE STATISTICS`.
- Evite `ORDER BY` global desnecessário (single reducer); prefira `DISTRIBUTE BY`/`SORT BY`.
- Saiba a diferença entre MANAGED e EXTERNAL e o efeito de `INSERT OVERWRITE`.

Veja `exemplo_particao.sql` para o padrão idiomático.
