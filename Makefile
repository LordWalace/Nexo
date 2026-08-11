.PHONY: install dev test test-backend test-mobile lint format typecheck migrate migration docker-up docker-down clean

install:
	@echo "Instalando dependências..."
	cd backend && poetry install
	npm install

dev: docker-up
	@echo "Iniciando ambiente de desenvolvimento..."
	@echo "Execute o backend em um terminal e o mobile em outro."

test: test-backend test-mobile

test-backend:
	@echo "Executando testes do backend..."
	cd backend && poetry run pytest --cov=app tests/

test-mobile:
	@echo "Executando testes do mobile..."
	cd apps/mobile && npm run test

lint:
	@echo "Executando lint..."
	cd backend && poetry run ruff check app tests
	cd apps/mobile && npm run lint

format:
	@echo "Executando formatação..."
	cd backend && poetry run ruff format app tests
	cd apps/mobile && npm run format

typecheck:
	@echo "Executando typecheck..."
	cd backend && poetry run mypy app
	cd apps/mobile && npm run typecheck

migrate:
	@echo "Aplicando migrações no banco de dados..."
	cd backend && poetry run alembic upgrade head

migration:
	@echo "Criando nova migração..."
	cd backend && poetry run alembic revision --autogenerate -m "auto"

docker-up:
	@echo "Subindo containers de infraestrutura..."
	docker-compose up -d

docker-down:
	@echo "Parando containers de infraestrutura..."
	docker-compose down

clean:
	@echo "Limpando arquivos temporários e de build..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf node_modules apps/*/node_modules
