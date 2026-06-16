---
applyTo: "**/*.sql"
description: Padrões de Teradata — QUALIFY, Primary/Partitioned Index e distribuição, skew, COLLECT STATS, SET/MULTISET e EXPLAIN.
---

# Instruções para Teradata

Complementa o pack `sql` com o que é específico do Teradata.

## Distribuição e índices

- A escolha do **Primary Index (PI)** define a distribuição entre AMPs — escolha colunas de alta cardinalidade e usadas em joins; nunca uma coluna com poucos valores (gera skew).
- Use **UPI** (único) quando a chave for única; **NUPI** quando não — mas evite NUPI com poucos valores distintos.
- Para tabelas grandes com filtro de intervalo (datas), use **PPI** (Partitioned Primary Index) e sempre filtre pela coluna de partição.
- Em joins, redistribuição/duplicação de spool acontece quando os PIs não casam; alinhe o PI das tabelas que se juntam com frequência.

## QUALIFY e funções analíticas

- Use `QUALIFY` para filtrar resultado de função de janela sem subquery: `QUALIFY ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...) = 1`.
- Prefira `ROW_NUMBER`/`RANK` + `QUALIFY` a `GROUP BY` + self-join para "última linha por chave".

## SET vs MULTISET

- `SET` (padrão em SQL puro) remove duplicatas a cada inserção — custa caro; use `MULTISET` quando duplicatas são impossíveis ou irrelevantes e o volume é alto.

## Estatísticas e EXPLAIN

- Rode `COLLECT STATISTICS` no PI, colunas de join e colunas de filtro; estatística desatualizada engana o otimizador.
- Leia o `EXPLAIN`: procure **product join** (sem condição de igualdade — quase sempre erro), redistribuição de spool grande e "low confidence".
- Tabelas temporárias: prefira **VOLATILE** (sessão) a tabelas físicas para intermediários; defina PI nelas também.

## Cuidados

- Evite função sobre a coluna de PI/partição no filtro — quebra o pruning e a estimativa.
- `TOP n` existe, mas para "n por grupo" use `QUALIFY` com `ROW_NUMBER`.
- Não fixe nomes de database/usuário no código; use parâmetros/variáveis de ambiente.
