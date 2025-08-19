help:
	@ehco "fwparser!"
lint:
	@scripts/linter.sh
test: lint
	@scripts/tests.sh
