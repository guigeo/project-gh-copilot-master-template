"""Busca polida: respeita robots.txt e aplica intervalo mínimo entre requisições.

Combine `RobotsCache` + `RateLimiter` + `http_client.get` para um crawl educado.
"""

from __future__ import annotations

import time
import urllib.robotparser
from urllib.parse import urljoin, urlparse

import httpx

from .http_client import DEFAULT_HEADERS, get


def _base_url(url: str) -> str:
    parts = urlparse(url)
    return f"{parts.scheme}://{parts.netloc}"


class RobotsCache:
    """Consulta e cacheia o robots.txt de cada domínio."""

    def __init__(self, user_agent: str = DEFAULT_HEADERS["User-Agent"]) -> None:
        self._user_agent = user_agent
        self._parsers: dict[str, urllib.robotparser.RobotFileParser] = {}

    def can_fetch(self, url: str) -> bool:
        base = _base_url(url)
        parser = self._parsers.get(base)
        if parser is None:
            parser = urllib.robotparser.RobotFileParser()
            parser.set_url(urljoin(base, "/robots.txt"))
            try:
                parser.read()
            except OSError:
                # robots.txt inacessível: trate como permissivo apenas se a
                # política do projeto permitir; aqui, por padrão, liberamos
                # mas registre essa decisão.
                parser.parse([])
            self._parsers[base] = parser
        return parser.can_fetch(self._user_agent, url)


class RateLimiter:
    """Garante um intervalo mínimo entre requisições (single-thread)."""

    def __init__(self, min_interval_s: float = 1.0) -> None:
        self._min_interval_s = min_interval_s
        self._last = 0.0

    def wait(self) -> None:
        elapsed = time.monotonic() - self._last
        if elapsed < self._min_interval_s:
            time.sleep(self._min_interval_s - elapsed)
        self._last = time.monotonic()


def fetch(
    client: httpx.Client,
    url: str,
    robots: RobotsCache,
    limiter: RateLimiter,
) -> httpx.Response:
    """Busca uma URL respeitando robots.txt e o rate limit.

    Levanta `PermissionError` se o robots.txt proibir o caminho.
    """
    if not robots.can_fetch(url):
        raise PermissionError(f"robots.txt proíbe acessar: {url}")
    limiter.wait()
    return get(client, url)
