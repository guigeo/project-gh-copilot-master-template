---
name: arcgis-arcpy-toolbox
description: Use esta skill para criar, revisar ou diagnosticar scripts ArcPy e automações no ArcGIS Pro.
---

Workflow ArcPy:

1. Confirmar versão do ArcGIS Pro.
2. Confirmar ambiente Python usado.
3. Validar entradas com `arcpy.Exists`.
4. Definir workspace e overwrite explicitamente.
5. Validar sistema de coordenadas.
6. Registrar parâmetros de entrada.
7. Executar ferramenta ArcPy.
8. Capturar mensagens com `arcpy.GetMessages()`.
9. Validar saída.
10. Logar tempo de execução.

Nunca recomendar instalação de `arcpy` via `pip`.
