"""Schemas pandera para validar DataFrames nas bordas do pipeline.

Valide o que entra (após a leitura) e o que sai (antes de persistir); não
confie na inferência de tipo em produção.
"""

from __future__ import annotations

# pandera >= 0.20 recomenda o namespace `pandera.pandas`; mantém-se o fallback
# para versões anteriores.
try:
    import pandera.pandas as pa
    from pandera.pandas import Check, Column, DataFrameSchema
except ModuleNotFoundError:  # pandera < 0.20
    import pandera as pa  # type: ignore[no-redef]
    from pandera import Check, Column, DataFrameSchema  # type: ignore[no-redef]

# Schema de exemplo: uma venda. Ajuste colunas/tipos ao seu domínio.
vendas_schema = DataFrameSchema(
    {
        "id_venda": Column("Int64", nullable=False, unique=True),
        "id_cliente": Column("Int64", nullable=False),
        "valor": Column(float, Check.ge(0), nullable=False),
        "dt_venda": Column("datetime64[ns]", nullable=False),
    },
    coerce=True,
    strict=False,
)


def validar_vendas(df: "pa.typing.DataFrame") -> "pa.typing.DataFrame":
    """Valida (e coage tipos de) um DataFrame de vendas; levanta se violar o schema."""
    return vendas_schema.validate(df)
