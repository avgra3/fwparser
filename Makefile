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
	@scripts/test_speedy.sh	
benchmark: lint
	@scripts/benchmark.sh	
chart_results: lint
	@scripts/chart_results.sh
