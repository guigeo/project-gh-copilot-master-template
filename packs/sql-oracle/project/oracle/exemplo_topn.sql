-- Objetivo: 10 maiores pedidos por valor no período
-- Fonte(s): pedidos (1 linha por pedido), particionada por dt_pedido
-- Granularidade: uma linha por id_pedido (top 10)
-- Filtros obrigatórios: dt_pedido entre binds (:inicio, :fim) -> partition pruning
-- Oracle: FETCH FIRST para top-N; bind variables evitam hard parse

SELECT
    p.id_pedido,
    p.id_cliente,
    p.valor,
    p.dt_pedido
FROM pedidos p
WHERE p.dt_pedido >= :inicio   -- bind: sem hard parse a cada valor
  AND p.dt_pedido <  :fim      -- intervalo na chave de partição: pruning
ORDER BY p.valor DESC
FETCH FIRST 10 ROWS ONLY;
