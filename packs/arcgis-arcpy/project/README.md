# Projeto ArcGIS / ArcPy

## Requisitos

- ArcGIS Pro instalado.
- Ambiente Python compatível com ArcGIS Pro.
- Não instalar `arcpy` via pip.

## Execução

O exemplo de geoprocessamento fica em `src/nome_pacote/geoprocessing.py`
(no mesmo pacote do projeto). Rode no Python do ArcGIS Pro:

```bash
python -m nome_pacote.geoprocessing
```

## Variáveis de ambiente

Configure caminhos e parâmetros em `.env`, não no código.

## Cuidados

- Validar sistema de coordenadas.
- Validar existência de entradas.
- Evitar sobrescrever dados sem confirmação.
- Registrar mensagens do ArcPy em logs.
