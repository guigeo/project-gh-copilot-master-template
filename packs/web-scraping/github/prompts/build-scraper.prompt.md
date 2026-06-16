---
mode: agent
description: Planeja e implementa um scraper responsável para um alvo, da estratégia ao parsing testável.
---

Quero raspar dados de: ${input:alvo:URL ou descrição do site e do dado desejado}

Antes de escrever código, siga a skill scraping-strategy e a resilient-crawling:

1. **Estratégia**: suba a escada de extração (dados oficiais → API → HTML estático → JS) e diga em que degrau vamos parar e por quê. Aponte robots.txt/ToS e a paginação.
2. **Plano**: liste os módulos a tocar — `http_client` (cliente), `fetch` (robots + rate limit + retry), `parse` (funções puras), `models` (registro) — e o critério de parada do crawl.
3. **Implementação**: escreva o código respeitando rate limit, retry só em transitórios, timeout explícito e parsing puro/testável. Seletores estáveis.
4. **Teste**: gere ao menos um teste de `parse` com HTML estático fixo (sem rede).
5. **Validação**: explique como rodar um lote pequeno primeiro e o que observar (taxa de erro, respeito ao rate limit, nº de registros).

Não implemente evasão de detecção nem raspe conteúdo atrás de login sem eu confirmar autorização. Peça confirmação antes de aumentar o volume.
