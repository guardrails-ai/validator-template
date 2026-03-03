.PHONY: dev lint test type qa

dev:
	pip install -e ".[dev]"

lint:
	ruff check .

test:
	pytest -v tests

type:
	pyright validator

qa:
	make lint
	make type
	make test
