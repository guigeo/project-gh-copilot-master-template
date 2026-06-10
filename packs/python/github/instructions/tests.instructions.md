---
applyTo: "tests/**/*.py,**/test_*.py,**/*_test.py"
description: Padrões de testes com pytest — determinismo, fixtures e cobertura de casos.
---

# Instruções para testes

- Use `pytest`.
- Testes devem ser pequenos, determinísticos e independentes.
- Evite depender de rede, banco real ou arquivos locais grandes.
- Use fixtures para dados de exemplo.
- Cubra casos felizes, nulos, erros esperados e limites.
- Não teste implementação interna quando o comportamento público for suficiente.
