.PHONY: install test lint format check

install:
	pip install -e .

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

check:
	ruff check .
	ruff format --check .
	pytest
