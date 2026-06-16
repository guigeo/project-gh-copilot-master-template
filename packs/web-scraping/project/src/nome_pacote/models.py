"""Tipos de registro extraído. Modele cada item com campos explícitos."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Item:
    """Um item raspado de uma página de listagem.

    Campos que podem faltar na origem são opcionais; valide o obrigatório
    (ex.: `url`) antes de persistir.
    """

    titulo: str
    url: str
    preco: float | None = None
