---
applyTo: "**/pipelines/**,**/etl/**,**/dags/**,**/*pipeline*.py,**/*etl*.py,**/*ingest*.py"
description: Padrões de engenharia de dados — pipelines incrementais, idempotência, particionamento e qualidade.
---

# Instruções para engenharia de dados

## Design de pipeline

- Antes de codificar, documente origem, destino, schema, volume estimado e frequência.
- Prefira processamento incremental a full reload; justifique quando full reload for necessário.
- Pipelines devem ser idempotentes: reexecutar não pode duplicar nem corromper dados.
- Separe ingestão, transformação, validação e escrita em etapas testáveis.

## Dados e formatos

- Prefira formatos colunares (Parquet) para dados analíticos; documente compressão e particionamento.
- Declare e versione o schema esperado; falhe com erro claro em schema drift inesperado.
- Particione por coluna de baixa cardinalidade usada em filtro (tipicamente data).
- Não carregue datasets inteiros em memória sem necessidade; use chunks ou pushdown.

## Qualidade

- Valide contagem, duplicidade por chave de negócio, nulos em colunas críticas e domínio de valores.
- Registre métricas de execução: linhas lidas/escritas, rejeitadas e tempo.
- Em falha parcial, prefira abortar com estado consistente a seguir silenciosamente.

## Segurança

- Credenciais de fontes/destinos via variáveis de ambiente ou secret manager, nunca no código.
- Não logue dados sensíveis; logue identificadores e contagens.
