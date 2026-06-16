-- Objetivo: última transação por cliente no mês de referência
-- Fonte(s): db.transacoes (1 linha por transacao)
-- Granularidade: uma linha por id_cliente
-- Chaves: id_cliente
-- Filtros obrigatórios: dt_referencia (coluna de partição / PPI)
-- Teradata: QUALIFY evita subquery; filtro literal na coluna de partição

SELECT
    id_cliente,
    id_transacao,
    valor,
    dt_transacao
FROM db.transacoes
WHERE dt_referencia >= DATE '2026-01-01'
  AND dt_referencia <  DATE '2026-02-01'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY id_cliente
    ORDER BY dt_transacao DESC
) = 1;
