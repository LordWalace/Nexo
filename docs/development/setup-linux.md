# Configuração do Ambiente de Desenvolvimento (Linux)

Este guia descreve os passos para rodar o backend no Linux usando Bash.

## Pré-requisitos
- Python 3.11 instalado
- Docker e Docker Compose instalados
- Bash (ou Zsh)

## Passos para Configuração
1. Na raiz do repositório, abra o terminal.
2. Execute o script de configuração:
   ```bash
   ./infrastructure/scripts/linux/setup-dev.sh
   ```
   Este script criará o ambiente virtual em `backend/.venv` e instalará todas as dependências.
3. Suba o Docker:
   ```bash
   ./infrastructure/scripts/linux/docker-up.sh
   ```
4. Aplique as migrações:
   ```bash
   ./infrastructure/scripts/linux/migrate-backend.sh
   ```
5. Inicie a API:
   ```bash
   ./infrastructure/scripts/linux/start-backend.sh
   ```

A API estará rodando em `http://localhost:8000`.

## Direnv (Recomendado)
O projeto suporta a ativação automática via `direnv`.
1. Instale o `direnv`.
2. Execute `direnv allow` na raiz do projeto.
Ele ativará automaticamente o ambiente em `backend/.venv`.
