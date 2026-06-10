"""Pipeline de Excel de referência: leitura validada, schema mínimo e escrita segura."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def validate_excel_input(path: str | Path) -> Path:
    excel_path = Path(path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Arquivo Excel não encontrado: {excel_path}")
    return excel_path


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")


def read_excel_sheet(
    path: str | Path,
    sheet_name: str,
    required_columns: list[str],
) -> pd.DataFrame:
    excel_path = validate_excel_input(path)
    workbook = pd.ExcelFile(excel_path, engine="openpyxl")
    if sheet_name not in workbook.sheet_names:
        raise ValueError(
            f"Worksheet '{sheet_name}' não existe em {excel_path.name}. "
            f"Abas disponíveis: {workbook.sheet_names}"
        )
    df = workbook.parse(sheet_name)
    validate_required_columns(df, required_columns)
    logger.info("Lidas %d linhas de %s!%s", len(df), excel_path.name, sheet_name)
    return df


def write_excel_safe(df: pd.DataFrame, path: str | Path, sheet_name: str = "dados") -> Path:
    """Escreve em arquivo temporário e renomeia; recusa sobrescrever destino existente."""
    out_path = Path(path)
    if out_path.exists():
        raise FileExistsError(f"Saída já existe e não será sobrescrita: {out_path}")
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    df.to_excel(tmp_path, sheet_name=sheet_name, index=False, engine="openpyxl")
    tmp_path.replace(out_path)
    logger.info("Gravadas %d linhas em %s", len(df), out_path)
    return out_path
