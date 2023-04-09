.PHONY: help
.DEFAULT_GOAL := help

help:
	python -m n2t --help

install: ## Install requirements
	pip install -r requirements.txt

format: ## Run code formatters
	isort tests
	black tests

lint: ## Run code linters
	isort --check tests
	black --check tests
	flake8 tests
	mypy tests

test:  ## Run tests with coverage
	pytest --cov