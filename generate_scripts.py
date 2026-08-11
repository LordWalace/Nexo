import os

windows_dir = "infrastructure/scripts/windows"
linux_dir = "infrastructure/scripts/linux"
os.makedirs(windows_dir, exist_ok=True)
os.makedirs(linux_dir, exist_ok=True)

windows_scripts = {
    "setup-dev.ps1": """$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$backend = Join-Path $root "backend"
$venv = Join-Path $backend ".venv"
$python = Join-Path $venv "Scripts/python.exe"

if (-not (Test-Path $venv)) {
    Write-Host "Criando ambiente virtual em backend/.venv..."
    python -m venv $venv
}

if (-not (Test-Path $python)) {
    throw "Python do ambiente virtual não foi encontrado."
}

& $python -m pip install --upgrade pip
& $python -m pip install -r "$backend/requirements-dev.txt"

Write-Host "Ambiente Windows configurado com sucesso."
""",
    "check-venv.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) {
    throw "Ambiente virtual não encontrado. Execute setup-dev.ps1"
}
Write-Host "Ambiente virtual OK."
""",
    "install-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
& $python -m pip install -r "$root/backend/requirements-dev.txt"
""",
    "start-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m uvicorn app.main:app --reload
""",
    "test-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m pytest tests/ -v --cov=app --cov-fail-under=80
""",
    "lint-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m ruff check app tests
""",
    "typecheck-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m mypy app
""",
    "format-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m ruff format app tests
""",
    "migrate-backend.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m alembic upgrade head
""",
    "create-migration.ps1": """param (
    [Parameter(Mandatory=$true)]
    [string]$Message
)
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m alembic revision --autogenerate -m "$Message"
""",
    "docker-up.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
Set-Location -Path $root
docker compose up -d
""",
    "docker-down.ps1": """$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
Set-Location -Path $root
docker compose down
"""
}

linux_scripts = {
    "setup-dev.sh": """#!/usr/bin/env bash
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
""",
    "check-venv.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then
    echo "Ambiente virtual não encontrado. Execute setup-dev.sh"
    exit 1
fi
echo "Ambiente virtual OK."
""",
    "install-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
"$PYTHON" -m pip install -r "$ROOT/backend/requirements-dev.txt"
""",
    "start-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m uvicorn app.main:app --reload
""",
    "test-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m pytest tests/ -v --cov=app --cov-fail-under=80
""",
    "lint-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m ruff check app tests
""",
    "typecheck-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m mypy app
""",
    "format-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m ruff format app tests
""",
    "migrate-backend.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m alembic upgrade head
""",
    "create-migration.sh": """#!/usr/bin/env bash
set -euo pipefail
if [ -z "${1-}" ]; then
  echo "Uso: $0 \\"mensagem da migração\\""
  exit 1
fi
MESSAGE="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON="$ROOT/backend/.venv/bin/python"
if [ ! -f "$PYTHON" ]; then echo "Ambiente virtual não encontrado."; exit 1; fi
cd "$ROOT/backend"
"$PYTHON" -m alembic revision --autogenerate -m "$MESSAGE"
""",
    "docker-up.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
docker compose up -d
""",
    "docker-down.sh": """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
docker compose down
"""
}

for name, content in windows_scripts.items():
    with open(os.path.join(windows_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

for name, content in linux_scripts.items():
    path = os.path.join(linux_dir, name)
    with open(path, "w", encoding="utf-8", newline='\n') as f:
        f.write(content)
    # on windows this might not set execute bits properly for linux, but we can try os.chmod
    try:
        os.chmod(path, 0o755)
    except:
        pass

print("Scripts criados com sucesso!")
