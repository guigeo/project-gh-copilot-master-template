---
applyTo: "**/*arcpy*.py,**/arcgis/**/*.py,**/gis/**/*.py,**/*.aprx,**/*.lyrx,**/*.gdb/**"
description: Padrões de ArcGIS Pro e ArcPy — ambiente, geoprocessamento, sistemas de coordenadas e logs.
---

# Instruções para ArcGIS e ArcPy

## Ambiente

- ArcPy deve ser executado no ambiente Python do ArcGIS Pro ou em cópia compatível desse ambiente.
- Não tente instalar `arcpy` via `pip`.
- Documente a versão do ArcGIS Pro usada.
- Evite hardcode de caminhos locais; use variáveis de ambiente ou arquivo `.env`.

## Geoprocessamento

- Sempre valide existência de entradas antes de executar ferramentas.
- Defina e verifique sistema de coordenadas.
- Registre workspace, geodatabase, feature class, campos críticos e SRID.
- Use `arcpy.env.overwriteOutput` de forma explícita.
- Para grandes volumes, prefira processar por lote quando possível.

## Dados espaciais

- Documente geometria esperada: ponto, linha ou polígono.
- Documente campos de latitude/longitude, ordem de coordenadas e datum.
- Para Brasil, confirme quando usar SIRGAS 2000, WGS84 ou projeções locais.
- Antes de spatial join/intersect, valide geometrias inválidas e projeções diferentes.

## Logs e erros

- Use logging estruturado.
- Capture mensagens do ArcPy com `arcpy.GetMessages()`.
- Ao falhar, informe ferramenta, parâmetros e dataset afetado.
