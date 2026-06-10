---
mode: agent
description: Desenha um pipeline de dados incremental e idempotente a partir de uma descrição de origem e destino.
---

Desenhe um pipeline de dados para a seguinte necessidade:

${input:descricao:Descreva origem, destino, volume aproximado e frequência desejada}

Responda com:

1. Origem, destino, schema e frequência (liste premissas assumidas).
2. Estratégia de carga: incremental vs full, chave de incremento e tratamento de atraso.
3. Particionamento e formato de armazenamento.
4. Etapas do pipeline (ingestão → transformação → validação → escrita) e idempotência de cada uma.
5. Validações de qualidade (use a skill `data-quality-checklist`).
6. Observabilidade: métricas e logs por execução.
7. Riscos e plano de reprocessamento.

Não implemente código ainda; entregue o desenho e aguarde confirmação.
