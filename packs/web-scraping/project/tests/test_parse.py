"""Testes do parsing com HTML estático fixo — sem rede."""

from nome_pacote.parse import parse_items

HTML = """
<html><body>
  <div class="item">
    <span class="titulo">Caderno</span>
    <span class="preco">R$ 19,90</span>
    <a href="/produto/caderno">ver</a>
  </div>
  <div class="item">
    <span class="titulo">Caneta</span>
    <!-- sem preço: campo opcional pode faltar -->
    <a href="/produto/caneta">ver</a>
  </div>
  <div class="item">
    <!-- sem título nem link: deve ser descartado -->
    <span class="preco">R$ 1,00</span>
  </div>
</body></html>
"""


def test_parse_items_extrai_e_normaliza() -> None:
    itens = parse_items(HTML, base_url="https://example.com")

    assert len(itens) == 2
    assert itens[0].titulo == "Caderno"
    assert itens[0].preco == 19.90
    assert itens[0].url == "https://example.com/produto/caderno"


def test_parse_items_campo_opcional_ausente() -> None:
    itens = parse_items(HTML, base_url="https://example.com")

    caneta = itens[1]
    assert caneta.titulo == "Caneta"
    assert caneta.preco is None
