from pathlib import Path

import pytest

import pandas as pd
from nome_pacote.excel_pipeline import (
    read_excel_sheet,
    validate_excel_input,
    validate_required_columns,
    write_excel_safe,
)


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"id": [1, 2], "valor": [10.5, 20.0]})


def test_validate_excel_input_raises_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "arquivo_inexistente.xlsx"

    with pytest.raises(FileNotFoundError):
        validate_excel_input(missing_path)


def test_validate_required_columns_raises_for_missing_column(sample_df: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="coluna_faltante"):
        validate_required_columns(sample_df, ["id", "coluna_faltante"])


def test_write_then_read_roundtrip(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    out_path = tmp_path / "saida.xlsx"

    write_excel_safe(sample_df, out_path, sheet_name="dados")
    df = read_excel_sheet(out_path, sheet_name="dados", required_columns=["id", "valor"])

    assert len(df) == len(sample_df)
    assert list(df.columns) == ["id", "valor"]


def test_read_excel_sheet_raises_for_missing_sheet(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    out_path = tmp_path / "saida.xlsx"
    write_excel_safe(sample_df, out_path)

    with pytest.raises(ValueError, match="aba_inexistente"):
        read_excel_sheet(out_path, sheet_name="aba_inexistente", required_columns=["id"])


def test_write_excel_safe_refuses_overwrite(tmp_path: Path, sample_df: pd.DataFrame) -> None:
    out_path = tmp_path / "saida.xlsx"
    write_excel_safe(sample_df, out_path)

    with pytest.raises(FileExistsError):
        write_excel_safe(sample_df, out_path)
