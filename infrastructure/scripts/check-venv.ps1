$ErrorActionPreference = "Stop"

$BackendPath = Join-Path -Path $PSScriptRoot -ChildPath "..\backend"
Set-Location -Path $BackendPath

if (-not (Test-Path -Path ".venv")) {
    Write-Host "❌ Erro: Ambiente virtual não encontrado em backend/.venv" -ForegroundColor Red
    Write-Host "💡 Correção: Execute 'python -m venv .venv' dentro da pasta backend/" -ForegroundColor Yellow
    exit 1
}

if (-not $env:VIRTUAL_ENV) {
    Write-Host "❌ Erro: Ambiente virtual não está ativo." -ForegroundColor Red
    Write-Host "💡 Correção: Certifique-se de ter instalado o direnv e executado 'direnv allow' na pasta backend/, ou ative manualmente com '.\.venv\Scripts\Activate.ps1'." -ForegroundColor Yellow
    exit 1
}

$PythonExec = Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
if (-not $PythonExec -match "\.venv") {
    Write-Host "❌ Erro: O executável do Python não pertence ao .venv!" -ForegroundColor Red
    Write-Host "Python atual: $PythonExec"
    exit 1
}

$PipExec = Get-Command pip -ErrorAction SilentlyContinue
if (-not $PipExec) {
    Write-Host "❌ Erro: pip não encontrado no ambiente virtual." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Sucesso: O ambiente virtual está configurado e ativo!" -ForegroundColor Green
Write-Host "🐍 Python: $PythonExec" -ForegroundColor Cyan
