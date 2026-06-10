# PySpark

Scaffold do tema PySpark.

## Estrutura

- `src/nome_pacote/session.py` — `get_spark()`: SparkSession única, reaproveitada em cluster.
- `src/nome_pacote/transformations.py` — transformações puras `DataFrame -> DataFrame`.
- `tests/conftest.py` — fixture `spark` local (`local[2]`, shuffle reduzido, UI desligada).

## Requisitos

- Java 17+ disponível no PATH (PySpark roda sobre a JVM).
- `uv sync` instala o PySpark; os testes rodam localmente sem cluster: `uv run pytest`.

## Convenções

- Lógica de transformação não faz I/O; leitura e escrita ficam nas bordas do pipeline.
- Em produção a sessão vem de `get_spark()`; `master("local[2]")` só existe na fixture de teste.
