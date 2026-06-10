# Projeto ArcGIS / ArcPy

## Requisitos

- ArcGIS Pro instalado.
- Ambiente Python compatível com ArcGIS Pro.
- Não instalar `arcpy` via pip.

## Execução

```bash
python src/arcpy_project/main.py
```

## Variáveis de ambiente

Configure caminhos e parâmetros em `.env`, não no código.

## Cuidados

- Validar sistema de coordenadas.
- Validar existência de entradas.
- Evitar sobrescrever dados sem confirmação.
- Registrar mensagens do ArcPy em logs.
