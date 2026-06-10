-- Objetivo: total de vendas por cliente ativo no mês de referência
-- Fonte(s): schema.vendas (1 linha por venda), schema.clientes (1 linha por cliente)
-- Destino: análise ad hoc
-- Granularidade: uma linha por id_cliente
-- Chaves: vendas.id_cliente -> clientes.id_cliente (N:1)
-- Filtros obrigatórios: vendas.dt_referencia (coluna de partição)

WITH vendas_mes AS (
    -- Agrega antes do join para garantir 1 linha por id_cliente
    SELECT
        id_cliente,
        SUM(valor) AS total_valor,
        COUNT(*) AS qtd_vendas
    FROM schema.vendas
    WHERE dt_referencia >= DATE '2026-01-01'
      AND dt_referencia < DATE '2026-02-01'
    GROUP BY id_cliente
),

clientes_ativos AS (
    SELECT
        id_cliente,
        nome_cliente
    FROM schema.clientes
    WHERE situacao = 'ATIVA'
)

SELECT
    c.id_cliente,
    c.nome_cliente,
    v.total_valor,
    v.qtd_vendas
FROM clientes_ativos AS c
INNER JOIN vendas_mes AS v
    ON v.id_cliente = c.id_cliente;
