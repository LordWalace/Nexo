$ErrorActionPreference = "Stop"

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
