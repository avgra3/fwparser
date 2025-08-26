help:
	@echo "fwparser!"
	@echo "Available commands: 'lint' and 'test'"
lint:
	@scripts/linter.sh
test: lint
	@scripts/tests.sh
test_large_data: lint
	@scripts/tests_large_data.sh
test_speedy: lint
	uv run pytest tests/test_speedy.py
