#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then
    echo "Ambiente virtual não encontrado. Execute setup-dev.sh"
    exit 1
fi
echo "Ambiente virtual OK."
