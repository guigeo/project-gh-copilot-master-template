-- Objetivo: página de pedidos por período, ordenados por data
-- Fonte(s): dbo.pedidos (1 linha por pedido)
-- Granularidade: uma linha por id_pedido
-- Filtros obrigatórios: dt_pedido (intervalo SARGable, sem função na coluna)
-- T-SQL: OFFSET/FETCH para paginação; índice sugerido para cobrir a query

-- Índice de cobertura recomendado:
--   CREATE NONCLUSTERED INDEX ix_pedidos_data
--     ON dbo.pedidos (dt_pedido) INCLUDE (id_cliente, valor);

DECLARE @inicio date = '2026-01-01';
DECLARE @fim    date = '2026-02-01';
DECLARE @pagina int  = 0;
DECLARE @tamanho int = 50;

SELECT
    p.id_pedido,
    p.id_cliente,
    p.valor,
    p.dt_pedido
FROM dbo.pedidos AS p
WHERE p.dt_pedido >= @inicio
  AND p.dt_pedido <  @fim   -- intervalo SARGable: usa o índice
ORDER BY p.dt_pedido
OFFSET (@pagina * @tamanho) ROWS
FETCH NEXT @tamanho ROWS ONLY;
