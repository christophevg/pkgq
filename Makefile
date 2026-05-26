# pkgq Makefile

.PHONY: help install test lint build publish clean

# Installation
help:
	@echo "pkgq - Package Query"
	@echo ""
	@echo "Commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make build      - Build package"
	@echo "  make publish    - Publish to PyPI"
	@echo "  make clean      - Clean build artifacts"

install:
	uv sync

test:
	uv run pytest -v

lint:
	uv run ruff check src/
	uv run mypy src/

build:
	uv build

publish: build
	uv publish

clean:
	rm -rf dist/
	rm -rf .venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete