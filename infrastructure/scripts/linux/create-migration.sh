#!/usr/bin/env bash
set -euo pipefail
if [ -z "${1-}" ]; then
  echo "Uso: $0 \"mensagem da migração\""
  exit 1
fi
MESSAGE="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m alembic revision --autogenerate -m "$MESSAGE"
