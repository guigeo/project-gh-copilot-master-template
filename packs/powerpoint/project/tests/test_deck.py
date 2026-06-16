"""Testes do deck lendo o modelo de objetos — sem abrir o PowerPoint."""

from io import BytesIO

import pandas as pd
from nome_pacote.charts import add_grafico_barras, add_tabela
from nome_pacote.content import resumo_kpis
from nome_pacote.deck import (
    add_bullets,
    add_capa,
    add_slide_visual,
    nova_apresentacao,
)


def test_estrutura_e_placeholders() -> None:
    prs = nova_apresentacao()
    add_capa(prs, "Relatório", "Junho/2026")
    add_bullets(prs, resumo_kpis(pd.DataFrame({"valor": [100.0, 300.0]})))

    assert len(prs.slides) == 2
    assert prs.slides[0].shapes.title.text == "Relatório"
    # KPIs viraram bullets no segundo slide
    corpo = prs.slides[1].placeholders[1].text_frame.text
    assert "Total: R$ 400.00" in corpo


def test_grafico_e_tabela_nativos() -> None:
    df = pd.DataFrame({"mes": ["jan", "fev"], "valor": [100, 200]})
    prs = nova_apresentacao()

    s1 = add_slide_visual(prs, "Vendas por mês")
    add_grafico_barras(s1, df, categoria="mes", valor="valor", titulo="Vendas")
    s2 = add_slide_visual(prs, "Detalhe")
    add_tabela(s2, df)

    assert any(shape.has_chart for shape in s1.shapes)
    assert any(shape.has_table for shape in s2.shapes)


def test_round_trip_em_memoria() -> None:
    prs = nova_apresentacao()
    add_capa(prs, "X")

    buffer = BytesIO()
    prs.save(buffer)

    # .pptx é um zip: começa com a assinatura "PK"
    assert buffer.getvalue()[:2] == b"PK"
