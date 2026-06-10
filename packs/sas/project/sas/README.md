# Programas SAS

Coloque aqui os programas `.sas` do projeto.

## Convenções

- Um programa por objetivo de negócio.
- Declare `libname` e `options` no topo.
- Use macro variáveis para caminhos e parâmetros de ambiente.
- Não versione credenciais nem strings de conexão.

## Estrutura sugerida

```text
sas/
├── README.md
├── exemplo.sas
├── macros/        # %MACRO reutilizáveis
└── jobs/          # programas executáveis
```
