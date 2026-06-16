"""Parsing puro: HTML (str) -> registros tipados. Sem rede, sem I/O.

Mantenha esta camada testável com HTML estático: a rede mora em `fetch`.
Ajuste os seletores ao site alvo; os daqui são um exemplo de listagem.
"""

from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .models import Item


def _texto(node, seletor: str) -> str | None:
    """Texto limpo do primeiro elemento que casa, ou None se ausente."""
    el = node.select_one(seletor)
    if el is None:
        return None
    texto = el.get_text(strip=True)
    return texto or None


def _preco(texto: str | None) -> float | None:
    """Converte '1.234,56' ou 'R$ 99,90' em float; None se não der."""
    if not texto:
        return None
    limpo = texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(limpo)
    except ValueError:
        return None


def parse_items(html: str, base_url: str = "") -> list[Item]:
    """Extrai itens de uma página de listagem.

    Cada item esperado em `.item`, com `.titulo`, `.preco` e um `<a href>`.
    Itens sem título ou sem link são descartados (caso normal, não erro).
    """
    soup = BeautifulSoup(html, "lxml")
    itens: list[Item] = []
    for node in soup.select(".item"):
        titulo = _texto(node, ".titulo")
        link = node.select_one("a[href]")
        if titulo is None or link is None:
            continue
        href = link.get("href", "")
        url = urljoin(base_url, href) if base_url else href
        itens.append(Item(titulo=titulo, url=url, preco=_preco(_texto(node, ".preco"))))
    return itens
