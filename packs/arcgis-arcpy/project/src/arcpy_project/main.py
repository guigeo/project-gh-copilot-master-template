from __future__ import annotations

import logging
import os
from pathlib import Path

try:
    import arcpy
except ImportError as exc:
    raise RuntimeError(
        "ArcPy não está disponível. Execute este script no ambiente Python do ArcGIS Pro."
    ) from exc

logger = logging.getLogger(__name__)


def validate_exists(path: str | Path) -> None:
    if not arcpy.Exists(str(path)):
        raise FileNotFoundError(f"Entrada não encontrada pelo ArcPy: {path}")


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    workspace = os.getenv("ARCGIS_WORKSPACE")
    if not workspace:
        raise ValueError("Defina ARCGIS_WORKSPACE no ambiente ou .env")

    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = False

    logger.info("Workspace ArcGIS configurado: %s", workspace)
    logger.info("Mensagens ArcPy: %s", arcpy.GetMessages())


if __name__ == "__main__":
    main()
