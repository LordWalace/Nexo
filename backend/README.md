# Nexo - Backend

Bem-vindo ao Backend do Nexo. O sistema é uma **API RESTful** construída com **Python** utilizando **FastAPI**, estruturada em princípios de Domain-Driven Design (DDD) e Clean Architecture, e utiliza PostgreSQL (Alembic para migrações) e Redis como tecnologias base.

## Pré-requisitos

Para rodar o backend localmente você precisará ter instalado:
- **Python 3.12+**
- **Docker e Docker Compose** (para subir o PostgreSQL e o Redis)
- Um gerenciador de ambientes como o `uv` (ou o módulo padrão `venv`)

## Como Baixar e Configurar

1. **Acesse a pasta do backend:**
   ```bash
   cd backend
   ```

2. **Crie e ative um Ambiente Virtual (venv):**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate
   
   # Linux/MacOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   # E caso queira contribuir:
   pip install -r requirements-dev.txt
   ```

4. **Configuração de Variáveis de Ambiente:**
   - Duplique o arquivo `.env.example` na raiz ou no backend (dependendo do escopo) renomeando-o para `.env`.
   - Modifique as variáveis (URL do banco de dados, JWT Secret, credenciais S3) para o seu ambiente local.

## Banco de Dados e Infraestrutura

O projeto possui um arquivo `docker-compose.yml` (geralmente na raiz do monorepo) para levantar o Postgres e o Redis.

1. **Suba os containers:**
   ```bash
   docker compose up -d
   ```

2. **Rode as migrações (Alembic):**
   Execute o seguinte comando para criar as tabelas no PostgreSQL:
   ```bash
   alembic upgrade head
   ```

## Como Rodar

Com o ambiente virtual ativado e as variáveis configuradas, inicie o servidor:

```bash
uvicorn app.main:app --reload
```

O backend estará disponível em: [http://localhost:8000](http://localhost:8000).  
A documentação iterativa (Swagger UI) estará disponível em: [http://localhost:8000/docs](http://localhost:8000/docs).

## Como Rodar Testes e Lint

Para manter a qualidade e os tipos corretos, antes de criar um PR, execute as seguintes ferramentas a partir da pasta `/backend`:

- **Testes**: `pytest` ou `pytest tests/`
- **Lint e Formatação**: `ruff check .` (e `ruff check . --fix` para auto-consertar)
- **Verificação de Tipos**: `mypy .`
