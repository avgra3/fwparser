help:
	@echo "fwparser!"
	@echo "Available commands: 'lint' and 'test'"
lint: format
	@scripts/linter.sh
format:
	@scripts/format.sh
test: lint
	@scripts/tests.sh
test_large_data: lint
	@scripts/tests_large_data.sh
test_speedy: lint
	@scripts/test_speedy.sh	
benchmark:  chart_results
	@scripts/benchmark.sh	
chart_results: lint
	@scripts/chart_results.sh
