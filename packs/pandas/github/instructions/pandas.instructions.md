---
applyTo: "**/*.py"
description: Padrões de pandas moderno — Copy-on-Write, dtypes anuláveis/Arrow, vetorização, merge validado e transformações puras testáveis.
---

# Instruções para pandas

Complementa o pack `python` com o que é específico de pandas (2.x/3.0).

## Copy-on-Write e atribuição

- Escreva código **CoW-safe**: habilite `pd.options.mode.copy_on_write = True` no início da aplicação (será o padrão no pandas 3.0).
- Nunca faça chained indexing para atribuir (`df[df.a > 0]["b"] = 1`); use `df.loc[df.a > 0, "b"] = 1`.
- Não use `inplace=True` (caminho de deprecação com CoW); reatribua o resultado (`df = df.assign(...)`).
- Trate o retorno das operações como novo objeto; não dependa de mutar uma "view".

## Dtypes

- Use **dtypes anuláveis** (`Int64`, `boolean`, `string`) para evitar `int` virar `float` ao aparecer `NA`.
- Prefira o **backend Arrow** (`dtype_backend="pyarrow"` na leitura) por memória e velocidade.
- Use `category` para colunas de baixa cardinalidade; declare `dtype`/`parse_dates`/`usecols` ao ler.
- Não confie em inferência de tipo em produção; valide o schema (pandera) nas bordas.

## Vetorização

- Não use `iterrows`, `itertuples` ou `apply(axis=1)` para lógica que vetoriza; prefira operações de coluna, `.str`/`.dt`, `np.where`, `np.select`.
- Não cresça DataFrame em loop com `concat`/`append` repetido; acumule em lista e concatene uma vez.
- Use `groupby(...).transform(...)` para devolver na granularidade original; `agg` para reduzir.

## Merge e NaN

- Em todo `merge`, declare `validate=` ("1:1"/"m:1"/"1:m") e use `indicator=True` para flagrar multiplicação de linhas e chaves órfãs.
- Lembre que `NaN != NaN`; `groupby` descarta grupos `NaN` por padrão (`dropna=False` para mantê-los).
- Cuidado com alinhamento por índice em operações entre Series/DataFrame; faça `reset_index` quando o índice não for chave.

## Engenharia e testabilidade

- Transformações são funções puras `DataFrame -> DataFrame`, sem I/O dentro; leitura e escrita ficam nas bordas (`io`).
- Encadeie com `.pipe(...)`; evite reatribuir `df` em dezenas de passos soltos.
- Teste com frames pequenos e `pd.testing.assert_frame_equal`; não use `print(df)` para depurar em produção, use `logging`.
- Prefira Parquet a CSV para dados intermediários; não fixe caminhos locais nem credenciais.

## Quando NÃO usar pandas

- Se os dados não cabem confortavelmente em memória (regra prática: > ~1/3 da RAM), considere processar em lotes ou migrar para Spark.
- `toPandas()`/coletar um DataFrame Spark grande para pandas é armadilha de OOM; só colete resultados já agregados.
