# Makefile with phony targets

.PHONY: setup lint format setup-hooks services
OS := $(shell uname)

setup: ## Setup Python Environment
	@make setup-git-hooks
	cp .env.example .env
	make services
	poetry install
	./resetdb.sh

services:
	if [ "$(OS)" = "Linux" ]; then \
		echo "Starting Linux services"; \
		sudo systemctl start rabbitmq-server; \
		sudo systemctl start redis; \
	elif [ "$(OS)" = "Darwin" ]; then \
		echo "Starting macOS services"; \
		brew services start rabbitmq; \
		brew services start redis; \
	else \
		echo "Unsupported operating system: $(OS)"; \
		exit 1; \
	fi

runserver: ## test
	@poetry run uvicorn --host 127.0.0.1 --port 8000 --reload config.asgi:application

test: ## test
	@ENVIRONMENT=test poetry run pytest

lint: ## Lint Python Files
	@poetry run ruff check .

format: ## Format Python Files
	@poetry run ruff check --fix .

setup-git-hooks: ## Setup Git Hook
	@echo "Setting up Git hooks..."
	cp .git-hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

generate-schema: ## Generate Schema
	@poetry run python manage.py generate_schema

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
