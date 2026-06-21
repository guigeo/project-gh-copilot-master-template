#!/usr/bin/env bash
# ===========================================================================
#  Cria um novo projeto a partir do template (macOS / Linux).
#  Precisa apenas de Python 3.11+ instalado. Nao usa uv.
#
#  Uso:
#    ./novo-projeto.sh                 -> abre o assistente interativo
#    ./novo-projeto.sh --list          -> lista os profiles
#    ./novo-projeto.sh --profile ...   -> repassa argumentos ao script
# ===========================================================================
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Procura um Python 3.11+ entre os nomes mais comuns.
PYBIN=""
for cand in python3.13 python3.12 python3.11 python3 python; do
    if command -v "$cand" >/dev/null 2>&1; then
        if "$cand" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
            PYBIN="$cand"
            break
        fi
    fi
done

if [ -z "$PYBIN" ]; then
    echo
    echo "Python 3.11+ nao encontrado."
    echo "Instale a partir de https://www.python.org/downloads/"
    echo "  (macOS: brew install python  |  Debian/Ubuntu: sudo apt install python3)"
    echo
    exit 1
fi

exec "$PYBIN" "$DIR/scripts/new_project.py" "$@"
