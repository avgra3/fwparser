.PHONY: lint format tests
lint:
	uv run --dev rff check --fix --verbose
format:
	uv run --dev ruff format
tests: format
	uv run --dev pytest tests --ignore-glob="bench/*.py"
benchmark: tests
	uv run --dev pytest tests/bench/large_dataset.py --capture=no
create-chart: tests
	uv run --dev python tests/bench/create_chart.py

