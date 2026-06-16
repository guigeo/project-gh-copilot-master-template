"""Teste do schema pandera de vendas."""

import pandas as pd
import pytest

from nome_pacote.schemas import validar_vendas


def test_validar_vendas_coage_tipos() -> None:
    df = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "id_cliente": [10, 11],
            "valor": [99.9, 10.0],
            "dt_venda": ["2026-01-01", "2026-01-02"],
        }
    )

    validado = validar_vendas(df)

    assert str(validado["id_venda"].dtype) == "Int64"
    assert str(validado["dt_venda"].dtype) == "datetime64[ns]"


def test_validar_vendas_rejeita_valor_negativo() -> None:
    df = pd.DataFrame(
        {
            "id_venda": [1],
            "id_cliente": [10],
            "valor": [-5.0],
            "dt_venda": ["2026-01-01"],
        }
    )

    with pytest.raises(Exception):  # SchemaError do pandera
        validar_vendas(df)
