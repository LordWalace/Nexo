import os

root = "nexo"

dirs = [
    "apps/mobile/app/(auth)",
    "apps/mobile/app/(tabs)",
    "apps/mobile/app/activities",
    "apps/mobile/app/categories",
    "apps/mobile/app/materials",
    "apps/mobile/app/history",
    "apps/mobile/app/statistics",
    "apps/mobile/app/devices",
    "apps/mobile/src/components/ui",
    "apps/mobile/src/components/forms",
    "apps/mobile/src/components/cards",
    "apps/mobile/src/components/feedback",
    "apps/mobile/src/components/layout",
    "apps/mobile/src/features/auth",
    "apps/mobile/src/features/activities",
    "apps/mobile/src/features/categories",
    "apps/mobile/src/features/materials",
    "apps/mobile/src/features/notifications",
    "apps/mobile/src/features/history",
    "apps/mobile/src/features/statistics",
    "apps/mobile/src/features/synchronization",
    "apps/mobile/src/features/devices",
    "apps/mobile/src/services/api",
    "apps/mobile/src/services/auth",
    "apps/mobile/src/services/notifications",
    "apps/mobile/src/services/storage",
    "apps/mobile/src/services/synchronization",
    "apps/mobile/src/services/uploads",
    "apps/mobile/src/hooks",
    "apps/mobile/src/stores",
    "apps/mobile/src/schemas",
    "apps/mobile/src/types",
    "apps/mobile/src/constants",
    "apps/mobile/src/theme",
    "apps/mobile/src/utils",
    "apps/mobile/src/config",
    "apps/mobile/assets",
    "apps/mobile/tests",
    "apps/web/src/components",
    "apps/web/src/features/auth",
    "apps/web/src/features/activities",
    "apps/web/src/features/categories",
    "apps/web/src/features/materials",
    "apps/web/src/features/notifications",
    "apps/web/src/features/history",
    "apps/web/src/features/statistics",
    "apps/web/src/features/synchronization",
    "apps/web/src/pages",
    "apps/web/src/layouts",
    "apps/web/src/services/api",
    "apps/web/src/services/auth",
    "apps/web/src/services/notifications",
    "apps/web/src/services/synchronization",
    "apps/web/src/hooks",
    "apps/web/src/stores",
    "apps/web/src/schemas",
    "apps/web/src/types",
    "apps/web/src/theme",
    "apps/web/src/utils",
    "apps/web/public",
    "apps/web/tests",
    "backend/app/core",
    "backend/app/api/v1",
    "backend/app/domain/entities",
    "backend/app/domain/value_objects",
    "backend/app/domain/repositories",
    "backend/app/domain/services",
    "backend/app/domain/exceptions",
    "backend/app/application/use_cases",
    "backend/app/application/dto",
    "backend/app/application/services",
    "backend/app/infrastructure/database/models",
    "backend/app/infrastructure/database/repositories",
    "backend/app/infrastructure/migrations",
    "backend/app/infrastructure/storage",
    "backend/app/infrastructure/notifications",
    "backend/app/infrastructure/oauth",
    "backend/app/infrastructure/cache",
    "backend/app/infrastructure/queue",
    "backend/app/schemas",
    "backend/app/workers",
    "backend/tests/unit/domain",
    "backend/tests/unit/application",
    "backend/tests/unit/services",
    "backend/tests/integration/api",
    "backend/tests/integration/database",
    "backend/tests/integration/repositories",
    "backend/tests/fixtures",
    "backend/alembic",
    "packages/api-contracts",
    "packages/shared-types",
    "packages/eslint-config",
    "tests/integration",
    "tests/e2e",
    "tests/fixtures",
    "infrastructure/docker",
    "infrastructure/nginx",
    "infrastructure/scripts",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "docs/architecture",
    "docs/api",
    "docs/development",
    "docs/testing"
]

files = {
    ".envrc": """if [ -d "backend/.venv" ]; then
  source backend/.venv/bin/activate
else
  echo "Ambiente virtual não encontrado."
  echo "Execute: python -m venv backend/.venv"
fi
""",
    ".env.example": """APP_NAME=Nexo API
APP_SLUG=nexo
APP_ENV=development
DEBUG=true

DATABASE_URL=postgresql+asyncpg://nexo_user:nexo_password@localhost:5432/nexo_db
REDIS_URL=redis://localhost:6379/0

JWT_SECRET_KEY=change-me
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

GOOGLE_CLIENT_ID=change-me
GOOGLE_CLIENT_SECRET=change-me
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

STORAGE_ENDPOINT=http://localhost:9000
STORAGE_ACCESS_KEY=nexo_access_key
STORAGE_SECRET_KEY=nexo_secret_key
STORAGE_BUCKET=nexo-materials

MAX_FILE_SIZE_MB=10
MAX_USER_STORAGE_MB=100
""",
    ".gitignore": """backend/.venv/
.venv/
venv/
ENV/
env/

__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

node_modules/
.expo/
dist/
build/

.env
.env.*
!.env.example

*.log
.DS_Store
""",
    ".editorconfig": """root = true
[*]
charset = utf-8
indent_style = space
indent_size = 2
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
[*.py]
indent_size = 4
""",
    ".pre-commit-config.yaml": """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
""",
    "CONTRIBUTING.md": "# Contributing to Nexo\n",
    "CODE_OF_CONDUCT.md": "# Code of Conduct\n",
    "LICENSE": "MIT License",
    "Makefile": """install:
\tnpm install
\tcd backend && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt

dev: docker-up dev-backend dev-mobile

dev-backend:
\tcd backend && .venv/Scripts/uvicorn app.main:app --reload

dev-mobile:
\tcd apps/mobile && npm run start

test: test-backend test-mobile test-web

test-backend:
\tcd backend && .venv/Scripts/pytest

test-mobile:
\tcd apps/mobile && npm run test

test-web:
\tcd apps/web && npm run test

lint:
\tcd backend && .venv/Scripts/ruff check .

format:
\tcd backend && .venv/Scripts/ruff format .

typecheck:
\tcd backend && .venv/Scripts/mypy .

migrate:
\tcd backend && .venv/Scripts/alembic upgrade head

migration:
\tcd backend && .venv/Scripts/alembic revision --autogenerate -m "auto"

docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down

check-venv:
\tpowershell infrastructure/scripts/check-venv.ps1

clean:
\trm -rf node_modules
\trm -rf backend/.venv
""",
    "package.json": """{
  "name": "nexo-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}
""",
    "README.md": """# Nexo — Aplicativo de Planejamento e Acompanhamento de Atividades

Este é o monorepo do Nexo.

## Setup

Criar o ambiente virtual (Windows):
```bash
python -m venv backend/.venv
```
Com o `direnv` (se instalado no bash/zsh/Powershell configurado):
```bash
direnv allow
```
Ou no PowerShell manualmente:
```powershell
.\\backend\\.venv\\Scripts\\Activate.ps1
```

## Docker e Serviços
```bash
docker-compose up -d
```
Isso iniciará `nexo-postgres`, `nexo-redis` e `nexo-minio`.

## Executando
API:
```bash
cd backend
.\\.venv\\Scripts\\uvicorn app.main:app --reload
```
Acesse `/docs`.
""",
    "docker-compose.yml": """version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: nexo-postgres
    environment:
      POSTGRES_USER: nexo_user
      POSTGRES_PASSWORD: nexo_password
      POSTGRES_DB: nexo_db
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    container_name: nexo-redis
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    container_name: nexo-minio
    command: server /data
    environment:
      MINIO_ROOT_USER: nexo_access_key
      MINIO_ROOT_PASSWORD: nexo_secret_key
    ports:
      - "9000:9000"
      - "9001:9001"
""",
    ".github/workflows/pull-request.yml": """name: Pull Request Pipeline
on:
  pull_request:
    branches:
      - main
      - develop
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          python -m venv backend/.venv
          source backend/.venv/bin/activate
          pip install -r backend/requirements.txt
          # ruff check
          # mypy
          # pytest --cov
""",
    ".github/pull_request_template.md": """## Descrição
Descreva o que foi alterado neste Pull Request.
""",
    "infrastructure/scripts/check-venv.ps1": """$venvPath = "backend/.venv"
if (Test-Path -Path $venvPath) {
    Write-Host "Ambiente virtual encontrado!" -ForegroundColor Green
} else {
    Write-Host "Ambiente virtual NAO encontrado em $venvPath!" -ForegroundColor Red
}
""",
    "infrastructure/scripts/check-venv.sh": """#!/bin/bash
if [ -d "backend/.venv" ]; then
    echo "Ambiente virtual encontrado!"
else
    echo "Ambiente virtual NAO encontrado!"
fi
""",
    "backend/app/main.py": """from fastapi import FastAPI

app = FastAPI(title="Nexo API")

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/health/database")
def health_db():
    return {"status": "ok"}

@app.get("/api/v1/health/redis")
def health_redis():
    return {"status": "ok"}
""",
    "backend/requirements.txt": """fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.11.0
asyncpg>=0.28.0
psycopg2-binary>=2.9.7
redis>=4.6.0
python-multipart>=0.0.6
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
ruff>=0.0.285
mypy>=1.5.0
pytest>=7.4.0
pytest-asyncio>=0.21.1
pytest-cov>=4.1.0
coverage>=7.3.0
httpx>=0.24.1
""",
    "backend/infrastructure/database/models/user.py": "# User Model",
    "backend/infrastructure/database/models/user_session.py": "# UserSession Model",
    "backend/infrastructure/database/models/user_consent.py": "# UserConsent Model",
    "backend/infrastructure/database/models/category.py": "# Category Model",
    "backend/infrastructure/database/models/material.py": "# Material Model",
    "backend/infrastructure/database/models/activity.py": "# Activity Model",
    "backend/infrastructure/database/models/activity_material.py": "# ActivityMaterial Model",
    "backend/infrastructure/database/models/activity_execution_period.py": "# ActivityExecutionPeriod Model",
    "backend/infrastructure/database/models/notification.py": "# Notification Model",
    "backend/infrastructure/database/models/device.py": "# Device Model",
    "docs/architecture/overview.md": "# Nexo — Aplicativo de Planejamento e Acompanhamento de Atividades\n",
    "docs/development/setup.md": "# Setup Nexo\n",
    "docs/testing/testing-strategy.md": "# Testing Nexo\n",
    "docs/api/api-versioning.md": "# API Versioning Nexo\n"
}

if not os.path.exists(root):
    os.makedirs(root)

for d in dirs:
    path = os.path.join(root, d)
    os.makedirs(path, exist_ok=True)

for f, content in files.items():
    path = os.path.join(root, f)
    # create parent directories for the file if they don't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

print("Scaffolding Nexo complete.")
