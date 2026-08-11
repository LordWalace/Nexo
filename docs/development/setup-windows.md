# Configuração do Ambiente de Desenvolvimento (Windows)

Este guia descreve os passos para rodar o backend no Windows usando PowerShell.

## Pré-requisitos
- Python 3.11 instalado
- Docker Desktop instalado
- PowerShell ou PowerShell 7

## Passos para Configuração
1. Na raiz do repositório, abra o PowerShell.
2. Execute o script de configuração:
   ```powershell
   .\infrastructure\scripts\windows\setup-dev.ps1
   ```
   Este script criará o ambiente virtual em `backend/.venv` e instalará todas as dependências.
3. Suba o Docker:
   ```powershell
   .\infrastructure\scripts\windows\docker-up.ps1
   ```
4. Aplique as migrações:
   ```powershell
   .\infrastructure\scripts\windows\migrate-backend.ps1
   ```
5. Inicie a API:
   ```powershell
   .\infrastructure\scripts\windows\start-backend.ps1
   ```

A API estará rodando em `http://localhost:8000`.

## Direnv (Opcional)
Se utilizar `direnv` para Windows, o `.envrc` na raiz já irá prover as instruções ou ativar automaticamente. No PowerShell, lembre-se de que a ativação nativa do script `.venv/Scripts/Activate.ps1` é suficiente se não for usar `direnv`.
