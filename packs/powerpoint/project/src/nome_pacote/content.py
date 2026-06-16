"""Camada de conteúdo: funções puras que transformam dados em specs de slide.

Sem python-pptx aqui e sem I/O — só decidem o QUE vai no slide. O builder
(`deck`) decide o COMO. Isso torna o conteúdo testável isoladamente.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(frozen=True, slots=True)
class SlideBullets:
    """Slide de título + tópicos."""

    titulo: str
    bullets: list[str] = field(default_factory=list)


def resumo_kpis(df: pd.DataFrame, coluna_valor: str = "valor") -> SlideBullets:
    """Gera um slide de KPIs a partir de um DataFrame de vendas já lido."""
    total = float(df[coluna_valor].sum())
    qtd = len(df)
    ticket = total / qtd if qtd else 0.0
    return SlideBullets(
        titulo="Resumo",
        bullets=[
            f"Total: R$ {total:,.2f}",
            f"Registros: {qtd:,}",
            f"Ticket médio: R$ {ticket:,.2f}",
        ],
    )
