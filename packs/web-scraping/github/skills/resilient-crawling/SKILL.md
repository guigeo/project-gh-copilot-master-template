---
name: resilient-crawling
description: Use esta skill para tornar um crawler educado e robusto — robots.txt, rate limiting, retry com backoff, retomada e tratamento responsável de bloqueios (429/403).
---

Um crawler de produção é, antes de tudo, **educado** e **retomável**. Aplique nesta ordem:

1. **robots.txt**: consulte com `urllib.robotparser` por domínio (cacheado) e respeite `Disallow`/`Crawl-delay`. Se um caminho é proibido, não acesse.
2. **Rate limiting**: garanta um intervalo mínimo entre requisições por domínio (ex.: 1 req/s). Para concorrência, limite requisições simultâneas por host; raspar não é teste de carga.
3. **Retry com backoff**: repita **só** erros transitórios — `429`, `5xx`, timeouts e erros de transporte. Backoff exponencial com jitter; honre o header `Retry-After` quando presente. **Não** repita `404`/`403`/`401`.
4. **Bloqueios (responsável)**: ao tomar `429`/`403` recorrente, **desacelere e pare** — aumente o intervalo, reduza concorrência ou interrompa. Não construa evasão de detecção (proxies rotativos, spoofing de browser, captcha solving) para contornar quem está te pedindo para parar.
5. **Timeouts**: todo request com `connect` e `read` timeout explícitos; um host lento não pode travar o crawl inteiro.
6. **Retomada/idempotência**: persista o progresso (URLs já coletadas / cursor) em checkpoint. Ao reexecutar, pule o que já foi feito e nunca duplique registros (chave de negócio).
7. **Caching local**: em desenvolvimento, cacheie respostas em disco para não re-bater no site a cada iteração do parser.
8. **Observabilidade**: logue por URL — status, tamanho, nº de registros extraídos e tempo. Conte sucessos vs. falhas; um pico de falhas significa "pare e investigue".

Meça antes de escalar: rode um lote pequeno, confirme a taxa de erro e o respeito ao rate limit, e só então aumente o volume.
