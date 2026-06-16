---
name: oracle-tuning
description: Use esta skill para diagnosticar e otimizar SQL/PL-SQL Oracle lento — plano real, estatísticas, bind variables, particionamento, índices e bulk PL/SQL.
---

Ao otimizar uma query Oracle, siga nesta ordem:

1. **Plano real**: use `DBMS_XPLAN.DISPLAY_CURSOR` (não só `EXPLAIN PLAN`) para ver o plano de fato executado, com linhas estimadas × reais (A-Rows × E-Rows). Divergência grande = estatística ruim.
2. **Estatísticas**: rode `DBMS_STATS.GATHER_TABLE_STATS` (com histogramas onde há skew de dados). Stats desatualizadas são a causa nº 1 de plano ruim.
3. **Bind variables**: troque literais por binds para evitar hard parse repetido; cuidado com *bind peeking* gerando plano instável (avalie adaptive cursor sharing).
4. **Índice e SARGability**: remova função/conversão implícita sobre coluna indexada; se a função é necessária, crie *function-based index*. Confira se o filtro está usando o índice no plano (INDEX RANGE SCAN vs FULL).
5. **Partition pruning**: confirme `PARTITION RANGE (ITERATOR/SINGLE)` no plano; filtre a chave de partição diretamente.
6. **Joins**: cheque o método (NESTED LOOPS para poucas linhas, HASH JOIN para volume); ordem de join ruim costuma ser sintoma de stats/cardinalidade erradas, não de falta de hint.
7. **Top-N**: `FETCH FIRST`/`ROW_NUMBER` em vez de `ROWNUM` mal posicionado.
8. **PL/SQL**: substitua loops linha a linha por `BULK COLLECT` + `FORALL`; meça a queda de context switches.
9. **Hints por último**: só depois de stats/índices, e documentando o porquê.

Valide equivalência com contagens/agregados antes e depois; meça por *buffer gets*/tempo no plano real.
