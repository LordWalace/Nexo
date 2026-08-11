$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "../../..")
$python = Join-Path $root "backend/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) {
    throw "Ambiente virtual não encontrado. Execute setup-dev.ps1"
}
Write-Host "Ambiente virtual OK."
