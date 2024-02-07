lint:
	ruff check .

tests:
	pytest ./test

type:
	pyright validator

qa:
	make lint
	make type
	make tests