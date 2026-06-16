"""Cliente HTTP com defaults sensatos para scraping: timeout, headers e retry.

A rede mora aqui e em `fetch`; o parsing (`parse`) fica puro e sem I/O.
"""

from __future__ import annotations

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential_jitter

# Identifique seu bot de forma honesta: nome real e uma forma de contato.
# Não finja ser um navegador para burlar bloqueio.
DEFAULT_HEADERS = {
    "User-Agent": "meu-scraper/0.1 (+https://example.com/sobre-o-bot; contato@example.com)",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

# connect curto, read um pouco maior; nenhum request fica sem timeout.
DEFAULT_TIMEOUT = httpx.Timeout(15.0, connect=5.0)

# Status transitórios que valem retry. 4xx como 403/404 NÃO entram aqui.
RETRYABLE_STATUS = frozenset({429, 500, 502, 503, 504})


class RetryableStatus(Exception):
    """Sinaliza um status transitório que deve acionar novo retry."""


def build_client(headers: dict[str, str] | None = None) -> httpx.Client:
    """Cria um `httpx.Client` com User-Agent identificável e timeouts explícitos."""
    return httpx.Client(
        headers={**DEFAULT_HEADERS, **(headers or {})},
        timeout=DEFAULT_TIMEOUT,
        follow_redirects=True,
    )


@retry(
    retry=retry_if_exception_type((httpx.TransportError, RetryableStatus)),
    wait=wait_exponential_jitter(initial=1.0, max=30.0),
    stop=stop_after_attempt(4),
    reraise=True,
)
def get(client: httpx.Client, url: str) -> httpx.Response:
    """GET com backoff exponencial + jitter, repetindo só erros transitórios.

    Levanta `RetryableStatus` em 429/5xx (aciona retry) e propaga 4xx
    permanentes via `raise_for_status` sem repetir.
    """
    response = client.get(url)
    if response.status_code in RETRYABLE_STATUS:
        raise RetryableStatus(f"{response.status_code} em {url}")
    response.raise_for_status()
    return response
