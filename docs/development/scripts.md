# Scripts de Desenvolvimento

Os scripts estão disponíveis em `infrastructure/scripts/windows/` (.ps1) e `infrastructure/scripts/linux/` (.sh). Use o equivalente do seu OS.

## Lista de Comandos

| Script | Descrição |
| --- | --- |
| `setup-dev` | Cria o ambiente `.venv` e instala dependências. |
| `check-venv` | Valida se o ambiente `.venv` existe. |
| `install-backend` | Reinstala os requirements caso haja alterações. |
| `start-backend` | Sobe o Uvicorn (`app.main:app --reload`). |
| `test-backend` | Roda `pytest` no backend. |
| `lint-backend` | Roda `ruff check` no backend. |
| `typecheck-backend` | Roda `mypy` no backend. |
| `format-backend` | Roda `ruff format` no backend. |
| `migrate-backend` | Roda `alembic upgrade head`. |
| `create-migration` | Gera uma migração. Ex: `create-migration -Message "Initial"`. |
| `docker-up` | Sobem os containers (`docker compose up -d`). |
| `docker-down` | Derrubam os containers. |

**Nota:** Os comandos utilizam estritamente o executável do ambiente virtual isolado em `backend/.venv/`. Nada é instalado ou roda de forma global no sistema operacional.
