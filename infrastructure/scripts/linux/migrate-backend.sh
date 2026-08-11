#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m alembic upgrade head
