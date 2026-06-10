---
name: data-quality-checklist
description: Use esta skill para validar qualidade de dados em pipelines — contagem, duplicidade, nulos, schema drift e reconciliação entre origem e destino.
---

Checklist de qualidade de dados:

1. **Contagem**: compare linhas lidas vs escritas; explique rejeições.
2. **Duplicidade**: valide unicidade da chave de negócio antes e depois de joins/merges.
3. **Nulos**: verifique colunas críticas; diferencie nulo legítimo de falha de parsing.
4. **Schema**: compare schema recebido com o declarado; alerte em colunas novas, removidas ou com tipo alterado.
5. **Domínio**: valide faixas e valores permitidos (datas plausíveis, valores não negativos, categorias conhecidas).
6. **Granularidade**: confirme que a tabela final tem a granularidade documentada (1 linha por chave).
7. **Reconciliação**: para cargas críticas, compare agregados (soma, contagem) entre origem e destino.
8. **Idempotência**: reexecute a carga em ambiente de teste e confirme que o resultado não muda.

Para cada verificação que falhar, registre métrica e interrompa antes de publicar no destino final.
