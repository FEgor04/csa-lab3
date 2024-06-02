all: format lint test

format:
	poetry run ruff format .

lint:
	poetry run ruff check . --unsafe-fixes --fix

test:
	poetry run pytest -v

