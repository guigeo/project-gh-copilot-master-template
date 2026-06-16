-- Objetivo: total de eventos por usuário no dia, com map join na dimensão
-- Fonte(s): db.eventos (particionada por dt), db.usuarios (dimensão pequena)
-- Granularidade: uma linha por id_usuario
-- Filtros obrigatórios: dt (coluna de partição, literal -> partition pruning)

SET hive.auto.convert.join=true;             -- habilita map join da dimensão
SET hive.vectorized.execution.enabled=true;  -- exige formato colunar (ORC/Parquet)

SELECT
    e.id_usuario,
    u.segmento,
    COUNT(*) AS qtd_eventos
FROM db.eventos AS e
JOIN db.usuarios AS u           -- tabela pequena: vira map join
    ON e.id_usuario = u.id_usuario
WHERE e.dt = '2026-01-15'       -- literal na coluna de partição: faz pruning
GROUP BY e.id_usuario, u.segmento;
