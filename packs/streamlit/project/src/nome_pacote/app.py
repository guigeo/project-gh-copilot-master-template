"""App Streamlit de exemplo.

Rode com:  streamlit run src/nome_pacote/app.py

Separa a camada de dados (função pura e cacheada) da camada de UI.
"""

from __future__ import annotations

import streamlit as st


@st.cache_data
def carregar_vendas() -> list[dict[str, object]]:
    """Fonte de dados da página.

    `cache_data` evita recarregar a cada rerun. Em um app real, troque por uma
    leitura de arquivo/query — mantendo-a aqui dentro para herdar o cache.
    """
    return [
        {"mes": "jan", "vendas": 120},
        {"mes": "fev", "vendas": 145},
        {"mes": "mar", "vendas": 132},
        {"mes": "abr", "vendas": 168},
    ]


def main() -> None:
    st.set_page_config(page_title="Painel de vendas", layout="wide")
    st.title("Painel de vendas")

    dados = carregar_vendas()
    total = sum(int(linha["vendas"]) for linha in dados)

    coluna_total, coluna_meses = st.columns(2)
    coluna_total.metric("Total de vendas", total)
    coluna_meses.metric("Meses", len(dados))

    st.bar_chart(dados, x="mes", y="vendas")
    st.dataframe(dados, use_container_width=True)


if __name__ == "__main__":
    main()
