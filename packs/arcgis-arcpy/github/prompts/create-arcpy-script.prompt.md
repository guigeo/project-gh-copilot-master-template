---
mode: agent
description: Cria um script ArcPy de geoprocessamento com validações de entrada, projeção e logging.
---

Crie um script ArcPy para a seguinte tarefa de geoprocessamento:

${input:tarefa:Descreva a tarefa, as camadas de entrada e a saída esperada}

Siga estes passos:

1. Liste entradas (feature classes, geometria, sistema de coordenadas) e a saída esperada.
2. Proponha a sequência de ferramentas ArcPy antes de codificar.
3. Implemente com: validação de entradas via `arcpy.Exists`, workspace e `overwriteOutput` explícitos, verificação de sistema de coordenadas, logging estruturado e captura de `arcpy.GetMessages()`.
4. Caminhos via variáveis de ambiente ou `.env`; nunca hardcoded.
5. Informe como executar no ambiente Python do ArcGIS Pro e como validar a saída.

Use a skill `arcgis-arcpy-toolbox` como referência. Não recomende instalar `arcpy` via pip.
