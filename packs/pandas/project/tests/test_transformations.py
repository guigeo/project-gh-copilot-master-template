"""Testes das transformações com frames pequenos e assert_frame_equal."""

import pytest
from pandas.testing import assert_frame_equal

import pandas as pd
from nome_pacote.transformations import (
    faixa_valor,
    juntar_clientes,
    normalizar_colunas,
    remover_duplicatas,
)


def test_normalizar_colunas() -> None:
    df = pd.DataFrame({"ID Cliente": [1], " Nome ": ["a"]})

    resultado = normalizar_colunas(df)

    assert list(resultado.columns) == ["id_cliente", "nome"]


def test_remover_duplicatas_mantem_mais_recente() -> None:
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "valor": ["antigo", "novo", "unico"],
            "atualizado_em": ["2024-01-01", "2024-06-01", "2024-03-01"],
        }
    )

    resultado = remover_duplicatas(df, chaves=["id"], coluna_ordem="atualizado_em")

    esperado = pd.DataFrame(
        {"id": [2, 1], "valor": ["unico", "novo"], "atualizado_em": ["2024-03-01", "2024-06-01"]}
    )
    assert_frame_equal(
        resultado.sort_values("id").reset_index(drop=True),
        esperado.sort_values("id").reset_index(drop=True),
    )


def test_faixa_valor_vetorizada() -> None:
    df = pd.DataFrame({"valor": [10.0, 500.0, 5000.0]})

    resultado = faixa_valor(df)

    assert resultado["faixa"].tolist() == ["baixo", "medio", "alto"]
    assert resultado["faixa"].dtype == "string"


def test_juntar_clientes_respeita_cardinalidade() -> None:
    vendas = pd.DataFrame({"id_venda": [1, 2], "id_cliente": [10, 10]})
    clientes = pd.DataFrame({"id_cliente": [10], "segmento": ["ouro"]})

    resultado = juntar_clientes(vendas, clientes)

    assert resultado["segmento"].tolist() == ["ouro", "ouro"]
    assert "_merge" not in resultado.columns


def test_juntar_clientes_falha_se_cliente_duplicado() -> None:
    vendas = pd.DataFrame({"id_venda": [1], "id_cliente": [10]})
    clientes_dup = pd.DataFrame({"id_cliente": [10, 10], "segmento": ["ouro", "prata"]})

    # validate="m:1" deve falhar: o lado direito não é único por id_cliente.
    with pytest.raises(pd.errors.MergeError):
        juntar_clientes(vendas, clientes_dup)
