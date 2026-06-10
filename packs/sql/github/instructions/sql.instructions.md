---
applyTo: "**/*.sql,**/sql/**/*.md"
description: Padrões de SQL — CTEs, joins, granularidade, filtros de partição e governança.
---

# Instruções para SQL

## Estilo

- Use CTEs para quebrar lógicas complexas.
- Nomeie CTEs de forma semântica.
- Evite `SELECT *` em queries de produção.
- Explicite colunas, filtros e regras de negócio.
- Padronize aliases curtos e claros.

## Segurança e governança

- Não concatene parâmetros diretamente em SQL gerado por aplicação.
- Evite expor dados sensíveis em logs ou tabelas temporárias persistentes.
- Documente origem, granularidade e chave de negócio.

## Performance

- Aplique filtros cedo.
- Evite funções em colunas usadas em filtros de partição quando isso impedir pruning.
- Cuidado com joins muitos-para-muitos.
- Verifique duplicidade antes e depois de joins críticos.
- Para tabelas particionadas, use filtros de partição sempre que possível.

## Revisão

Ao revisar SQL, verifique:

- Chaves de join.
- Risco de duplicidade.
- Filtros de data/partição.
- Regra de nulos.
- Granularidade final.
- Custo/performance.
