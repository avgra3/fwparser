VERBOSE ?= ""

.PHONY: lint format tests
lint:
	uv run --dev ruff check --fix
format:
	uv run --dev ruff format
type-check: format
	uv run --dev ty check
tests: type-check
	uv run --dev pytest tests --ignore-glob="bench/*.py" $(VERBOSE)
benchmark: tests
	uv run --dev pytest tests/bench/large_dataset.py --capture=no
create-chart: tests
	uv run --dev python tests/bench/create_chart.py

