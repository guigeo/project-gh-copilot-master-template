---
name: teradata-tuning
description: Use esta skill para diagnosticar e otimizar SQL Teradata lento ou caro — skew, spool, product joins, estatísticas e índices PI/PPI.
---

Ao otimizar uma query Teradata, siga nesta ordem:

1. **EXPLAIN primeiro**: rode `EXPLAIN` e classifique cada passo. Sinais de alarme: *product join*, *duplicated to all AMPs* de tabela grande, *redistributed by* repetido, "no confidence"/"low confidence".
2. **Estatísticas**: confirme `COLLECT STATISTICS` recente no PI, colunas de join e de filtro. Sem stats, o otimizador chuta — corrija isto antes de qualquer outra coisa.
3. **Skew**: se um AMP recebe muito mais linhas (CPU/spool desbalanceado), o PI está mal escolhido. Cheque a cardinalidade da coluna de PI; redistribua ou troque o PI.
4. **Spool**: spool estourando = redistribuição cara. Alinhe PIs das tabelas que se juntam, agregue antes do join e reduza colunas/linhas cedo.
5. **Product join**: quase sempre é condição de join ausente ou tipo incompatível forçando comparação não-igualdade. Corrija a condição.
6. **Partição (PPI)**: confirme que o filtro atinge a coluna de partição como literal (sem função em volta) para haver partition elimination.
7. **QUALIFY**: troque subqueries de "última linha por chave" por `QUALIFY ROW_NUMBER()`; menos passos no plano.
8. **Volatile tables**: materialize intermediários reutilizados em VOLATILE com PI adequado em vez de reprocessar.

Meça antes/depois pelo `EXPLAIN` e pelo tempo/CPU; registre o ganho de cada mudança.
