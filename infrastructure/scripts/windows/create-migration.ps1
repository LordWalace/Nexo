param (
    [Parameter(Mandatory=$true)]
    [string]$Message
)
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) { throw "Ambiente virtual não encontrado." }
Set-Location -Path (Join-Path $root "backend")
& $python -m alembic revision --autogenerate -m "$Message"
