---
applyTo: "**/*.py"
description: Padrões de web scraping — ética/robots, requisição polida, retry/backoff, parsing puro e testável, e dados validados.
---

# Instruções para Web Scraping

## Ética e legalidade (inegociável)

- Respeite `robots.txt` e os Termos de Uso do site; não raspe conteúdo atrás de login sem autorização explícita.
- Identifique o bot num `User-Agent` real, com forma de contato; nunca se passe por navegador para burlar bloqueio.
- Prefira fonte oficial: API pública, feed, `sitemap.xml` ou download de dados antes de raspar HTML.
- Não colete dados pessoais sem base legal; ao tratar PII, minimize e documente a finalidade.

## Requisição

- Use um cliente único (`build_client()`), com `timeout` explícito e `follow_redirects` controlado; nunca requisição sem timeout.
- Centralize headers (`User-Agent`, `Accept-Language`) no cliente; não espalhe headers soltos pelo código.
- Não fixe cookies, tokens ou sessões autenticadas no código; venham de configuração externa.

## Robustez

- Aplique rate limiting (intervalo mínimo entre requisições); raspar não é teste de carga.
- Use retry com backoff exponencial **apenas** para erros transitórios (429, 5xx, timeout); respeite `Retry-After`. Não repita 4xx como 404/403.
- Torne o crawl retomável: registre o que já foi coletado (checkpoint) e seja idempotente ao reprocessar.
- Trate encoding explicitamente (`response.encoding`/charset); não assuma UTF-8 cego.

## Parsing

- Separe rede de extração: funções de parsing são puras `str (HTML) -> registros`, sem I/O nem requisição dentro.
- Prefira seletores estáveis (atributos semânticos, `data-*`, ids) a caminhos frágeis dependentes de layout.
- Trate ausência de elemento como caso normal (retorne `None`/pule), não com exceção não tratada.
- Para conteúdo renderizado por JS, só então use navegador headless (Playwright); não é o caminho padrão.

## Dados

- Modele cada registro com um tipo explícito (`dataclass`) e valide campos obrigatórios antes de persistir.
- Deduplique por chave de negócio e normalize (trim, casas decimais, datas em ISO-8601).
- Persista de forma incremental (NDJSON/CSV/Parquet por lote); não acumule tudo em memória.

## Testabilidade

- Teste o parsing com HTML estático fixo (sem rede); a rede entra só em testes de integração marcados.
- Não use `print` para depurar coleta em produção; use `logging` com contagens e URLs.
