# Web Scraping

Scaffold do tema de raspagem de dados, responsável e testável.

## Estrutura

- `src/nome_pacote/http_client.py` — `build_client()` (User-Agent honesto, timeouts) e `get()` (retry com backoff só em 429/5xx/timeout).
- `src/nome_pacote/fetch.py` — `RobotsCache` (respeita robots.txt) + `RateLimiter` (intervalo mínimo) + `fetch()`.
- `src/nome_pacote/parse.py` — funções puras `HTML -> registros`, sem rede; troque os seletores pelo site alvo.
- `src/nome_pacote/models.py` — `Item`: registro tipado, campos opcionais quando a origem pode faltar.
- `tests/test_parse.py` — parsing testado com HTML estático fixo (sem rede).

## Fluxo

1. `scraping-strategy`: escolha o degrau de extração (dados oficiais → API → HTML estático → JS).
2. `fetch()` busca de forma educada (robots + rate limit + retry).
3. `parse_*()` transforma o HTML em registros tipados.
4. Valide, deduplique por chave e persista de forma incremental (NDJSON/CSV/Parquet).

## Requisitos

- `uv sync` instala httpx, BeautifulSoup, lxml e tenacity.
- Páginas que só renderizam por JavaScript: `uv sync --group dynamic` e `uv run playwright install chromium`. Use Playwright só quando o dado não vem no HTML inicial.
- Testes rodam sem rede: `uv run pytest`.

## Responsabilidade

- Respeite robots.txt e os Termos de Uso; identifique o bot e ofereça contato.
- Rate limit sempre; ao tomar 429/403, desacelere e pare — não construa evasão de bloqueio.
- Não raspe conteúdo atrás de login sem autorização nem colete PII sem base legal.
