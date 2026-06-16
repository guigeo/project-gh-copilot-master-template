# pandas

Scaffold do tema pandas moderno (2.x/3.0), com transformações puras e testáveis.

## Estrutura

- `src/nome_pacote/transformations.py` — funções puras `DataFrame -> DataFrame` (CoW-safe), com `merge` validado (`validate="m:1"`) e exemplo vetorizado (`np.select`).
- `src/nome_pacote/schemas.py` — schema pandera de exemplo; valide nas bordas, não confie em inferência.
- `src/nome_pacote/io.py` — leitura/escrita nas bordas: `usecols`/`dtype`/`parse_dates`, backend Arrow e Parquet.
- `tests/` — `assert_frame_equal` em frames pequenos + teste de cardinalidade e de schema.

## Convenções

- Habilite Copy-on-Write no início da app: `pd.options.mode.copy_on_write = True` (padrão no pandas 3.0).
- Atribua com `.loc`; nunca chained indexing; não use `inplace=True`.
- Dtypes anuláveis (`Int64`, `string`) e `category`/Arrow para memória.
- Todo `merge` com `validate=` e `indicator=True`.
- Lógica sem I/O; leitura/escrita só em `io`.

## Requisitos

- `uv sync` instala pandas, pyarrow e pandera.
- Testes rodam sem I/O externo: `uv run pytest`.

## Quando NÃO usar pandas

- Dataset não cabe em memória (> ~1/3 da RAM) ou job vive estourando → processe em lotes ou migre o pesado para Spark; use pandas só no resultado já agregado.
