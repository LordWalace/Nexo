import os
import textwrap

root = "study-app"

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
    "apps/mobile/src/services/api/endpoints",
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
    "apps/mobile/assets/images",
    "apps/mobile/assets/icons",
    "apps/mobile/assets/fonts",
    "apps/mobile/assets/animations",
    "apps/mobile/tests/components",
    "apps/mobile/tests/screens",
    "apps/mobile/tests/hooks",
    "apps/mobile/tests/services",
    "apps/mobile/tests/stores",
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
    "backend/.venv",
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
    # Root files
    ".envrc": """if [ -d "backend/.venv" ]; then
  source backend/.venv/bin/activate
else
  echo "Ambiente virtual não encontrado."
  echo "Execute: python -m venv backend/.venv"
fi
""",
    ".env.example": """# Shared ENVs
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=studyapp
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0

MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_URL=http://minio:9000
""",
    ".gitignore": """node_modules/
.venv/
__pycache__/
*.pyc
.env
dist/
build/
.expo/
coverage/
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
    "CONTRIBUTING.md": "# Contributing\n\n1. Branch from develop.\n2. Submit PR.",
    "CODE_OF_CONDUCT.md": "# Code of Conduct\n\nBe respectful.",
    "LICENSE": "MIT License",
    "Makefile": """install:
\tnpm install
\tcd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

dev: docker-up dev-backend dev-mobile

dev-backend:
\tcd backend && . .venv/bin/activate && uvicorn app.main:app --reload

dev-mobile:
\tcd apps/mobile && npm run start

test: test-backend test-mobile test-web

test-backend:
\tcd backend && . .venv/bin/activate && pytest

test-mobile:
\tcd apps/mobile && npm run test

test-web:
\tcd apps/web && npm run test

lint:
\t# run linter

format:
\t# run formatter

typecheck:
\t# run typecheck

migrate:
\tcd backend && . .venv/bin/activate && alembic upgrade head

migration:
\tcd backend && . .venv/bin/activate && alembic revision --autogenerate -m "auto"

docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down

check-venv:
\t@test -d backend/.venv || echo "Virtual env not found in backend/.venv"

clean:
\trm -rf node_modules
\trm -rf backend/.venv
""",
    "package.json": """{
  "name": "study-app-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}
""",
    "README.md": """# Study App

A monorepo for Study App.

## Setup
```bash
python -m venv backend/.venv
direnv allow
```
""",
    "docker-compose.yml": """version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
      POSTGRES_DB: ${POSTGRES_DB:-studyapp}
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    command: server /data
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin}
    ports:
      - "9000:9000"
      - "9001:9001"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - minio
""",

    # .github files
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
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Create Venv & Install
        run: |
          python -m venv backend/.venv
          source backend/.venv/bin/activate
          pip install -r backend/requirements.txt
      - name: Lint, Typecheck, Test
        run: |
          source backend/.venv/bin/activate
          # ruff check backend/
          # mypy backend/
          # pytest backend/ --cov=backend

  mobile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: cd apps/mobile && npm run lint && npm run test

  web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: cd apps/web && npm run lint && npm run test

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo "Run security scans (gitleaks, npm audit, pip-audit)"
""",
    ".github/workflows/deploy.yml": """name: Deploy
on:
  push:
    branches:
      - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy..."
""",
    ".github/pull_request_template.md": """## Descrição

Descreva o que foi alterado.

## Tipo de alteração

- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Refatoração
- [ ] Testes
- [ ] Documentação
- [ ] Infraestrutura

## Requisitos relacionados

Informe os requisitos funcionais ou não funcionais relacionados.

## Testes realizados

- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Testes manuais
- [ ] Testes de interface

Comandos executados:

```bash
# comandos utilizados
```

## Checklist

- [ ] O código segue o padrão do projeto.
- [ ] Foram adicionados ou atualizados testes.
- [ ] O lint foi executado.
- [ ] O typecheck foi executado.
- [ ] A documentação foi atualizada.
- [ ] Não foram adicionados secrets.
- [ ] O pipeline foi executado com sucesso.
- [ ] A alteração não quebra funcionalidades existentes.
""",

    # Backend base files
    "backend/app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()",
    "backend/app/core/config.py": "# config",
    "backend/app/core/security.py": "# security",
    "backend/app/core/logging.py": "# logging",
    "backend/app/core/dependencies.py": "# dependencies",
    "backend/app/api/router.py": "# router",
    "backend/app/api/v1/router.py": "# v1 router",
    "backend/app/api/v1/auth.py": "# auth",
    "backend/app/api/v1/users.py": "# users",
    "backend/app/api/v1/categories.py": "# categories",
    "backend/app/api/v1/materials.py": "# materials",
    "backend/app/api/v1/activities.py": "# activities",
    "backend/app/api/v1/notifications.py": "# notifications",
    "backend/app/api/v1/history.py": "# history",
    "backend/app/api/v1/statistics.py": "# stats",
    "backend/app/infrastructure/database/session.py": "# session",
    "backend/app/infrastructure/database/base.py": "# base",
    "backend/tests/conftest.py": "# pytest fixtures",
    "backend/alembic.ini": "# alembic config",
    "backend/pyproject.toml": "[tool.poetry]\nname=\"backend\"\n",
    "backend/Dockerfile": "FROM python:3.11\nCMD [\"uvicorn\", \"app.main:app\"]",
    "backend/.env.example": "# backend envs",
    "backend/README.md": "# Backend\n",
    "backend/requirements.txt": "fastapi\npytest\n",

    # Mobile base files
    "apps/mobile/app/_layout.tsx": "export default function Layout() { return null; }",
    "apps/mobile/app/index.tsx": "export default function Index() { return null; }",
    "apps/mobile/app/(auth)/_layout.tsx": "",
    "apps/mobile/app/(auth)/login.tsx": "",
    "apps/mobile/app/(auth)/register.tsx": "",
    "apps/mobile/app/(auth)/verify-email.tsx": "",
    "apps/mobile/app/(auth)/forgot-password.tsx": "",
    "apps/mobile/app/(auth)/reset-password.tsx": "",
    "apps/mobile/app/(tabs)/_layout.tsx": "",
    "apps/mobile/app/(tabs)/index.tsx": "",
    "apps/mobile/app/(tabs)/agenda.tsx": "",
    "apps/mobile/app/(tabs)/materials.tsx": "",
    "apps/mobile/app/(tabs)/progress.tsx": "",
    "apps/mobile/app/(tabs)/settings.tsx": "",
    "apps/mobile/app/activities/index.tsx": "",
    "apps/mobile/app/activities/create.tsx": "",
    "apps/mobile/app/activities/[id].tsx": "",
    "apps/mobile/app/activities/edit.tsx": "",
    "apps/mobile/app/categories/index.tsx": "",
    "apps/mobile/app/categories/create.tsx": "",
    "apps/mobile/app/categories/[id].tsx": "",
    "apps/mobile/app/categories/edit.tsx": "",
    "apps/mobile/app/materials/index.tsx": "",
    "apps/mobile/app/materials/create.tsx": "",
    "apps/mobile/app/materials/[id].tsx": "",
    "apps/mobile/app/materials/edit.tsx": "",
    "apps/mobile/app/history/index.tsx": "",
    "apps/mobile/app/history/[id].tsx": "",
    "apps/mobile/app/statistics/index.tsx": "",
    "apps/mobile/app/statistics/by-category.tsx": "",
    "apps/mobile/app/devices/index.tsx": "",
    "apps/mobile/src/services/api/client.ts": "",
    "apps/mobile/src/services/api/interceptors.ts": "",
    "apps/mobile/src/theme/colors.ts": "",
    "apps/mobile/src/theme/typography.ts": "",
    "apps/mobile/src/theme/spacing.ts": "",
    "apps/mobile/src/theme/light-theme.ts": "",
    "apps/mobile/src/theme/dark-theme.ts": "",
    "apps/mobile/src/theme/index.ts": "",
    "apps/mobile/app.json": "{}",
    "apps/mobile/babel.config.js": "module.exports = {};",
    "apps/mobile/metro.config.js": "module.exports = {};",
    "apps/mobile/package.json": '{"name": "mobile", "scripts": {"start": "expo start"}}',
    "apps/mobile/tsconfig.json": "{}",
    "apps/mobile/jest.config.js": "module.exports = {};",
    "apps/mobile/eslint.config.js": "module.exports = [];",
    "apps/mobile/prettier.config.js": "module.exports = {};",
    "apps/mobile/.env.example": "# mobile envs",

    # Web base files
    "apps/web/package.json": '{"name": "web"}',
    "apps/web/tsconfig.json": "{}",
    "apps/web/eslint.config.js": "module.exports = [];",
    "apps/web/prettier.config.js": "module.exports = {};",
    "apps/web/.env.example": "# web envs",

    # Documentation files
    "docs/architecture/overview.md": "# Architecture Overview",
    "docs/development/setup.md": "# Setup",
    "docs/development/commands.md": "# Commands",
    "docs/testing/testing-strategy.md": "# Testing Strategy",
    "docs/testing/pull-request-flow.md": "# Pull Request Flow",
    "docs/api/api-versioning.md": "# API Versioning",
}

if not os.path.exists(root):
    os.makedirs(root)

for d in dirs:
    path = os.path.join(root, d)
    os.makedirs(path, exist_ok=True)

for f, content in files.items():
    path = os.path.join(root, f)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

print("Scaffolding complete.")
