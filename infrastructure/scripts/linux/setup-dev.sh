#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
BACKEND="$ROOT/backend"
VENV="$BACKEND/.venv"
PYTHON="$VENV/bin/python"

if [ ! -d "$VENV" ]; then
  echo "Criando ambiente virtual em backend/.venv..."
  python3 -m venv "$VENV"
fi

if [ ! -f "$PYTHON" ]; then
  echo "Python do ambiente virtual não foi encontrado."
  exit 1
fi

"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install -r "$BACKEND/requirements-dev.txt"

echo "Ambiente Linux configurado com sucesso."
