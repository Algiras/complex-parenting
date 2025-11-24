.PHONY: help lint-check scan-chars install install-dev clean test coverage lint format pre-commit-install pre-commit-run

help:
	@echo "Available commands:"
	@echo "  make install           - Install the project in production mode"
	@echo "  make install-dev       - Install the project with development dependencies"
	@echo "  make lint-check        - Run markdown lint checker on book content"
	@echo "  make scan-chars        - Scan for invalid characters in book files"
	@echo "  make test              - Run all tests"
	@echo "  make coverage          - Run tests with coverage report"
	@echo "  make lint              - Run ruff linter"
	@echo "  make format            - Format code with ruff"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make pre-commit-run    - Run pre-commit on all files"
	@echo "  make clean             - Remove build artifacts and cache files"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint-check:
	python -m scripts.lint_check

scan-chars:
	python -m scripts.scan_chars

test:
	python -m pytest

coverage:
	python -m pytest --cov=scripts --cov-report=html --cov-report=term-missing

lint:
	python -m ruff check .

format:
	python -m ruff format .
	python -m ruff check --fix .

pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/
