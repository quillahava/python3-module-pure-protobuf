# Please follow the Makefile style guide.
# http://clarkgrubb.com/makefile-style-guide

BIN := venv/bin

.PHONY: build
build:
	$(BIN)/python -m build --sdist --wheel

.PHONY: publish
publish:
	$(BIN)/python -m twine upload dist/*

.PHONY: clean
clean:
	find . -type d -name __pycache__ -delete
	rm -rf venv .mypy_cache .pytest_cache build dist *.egg-info .coverage .benchmarks

.PHONY: venv
venv:
	python3 -m venv venv
	$(BIN)/pip install --upgrade pip wheel
	$(BIN)/pip install -e.[dev]

.PHONY: test check
test check: unittests lint

.PHONY: unittests
unittests:
	$(BIN)/coverage run --source=pure_protobuf -m pytest --benchmark-disable tests
	$(BIN)/coverage lcov -o .coverage.lcov
	$(BIN)/coverage xml -o .coverage.xml
	$(BIN)/coverage html -d .coverage.html

.PHONY: benchmark
benchmark:
	$(BIN)/pytest --benchmark-only --benchmark-columns=mean,stddev,median,ops --benchmark-warmup=on tests

.PHONY: format
format: format/isort format/black

.PHONY: format/isort
format/isort:
	$(BIN)/isort pure_protobuf tests

.PHONY: format/black
format/black:
	$(BIN)/black pure_protobuf tests

.PHONY: lint
lint: lint/flake8 lint/isort lint/mypy lint/format

.PHONY: lint/flake8
lint/flake8:
	$(BIN)/flake8 pure_protobuf tests

.PHONY: lint/isort
lint/isort:
	$(BIN)/isort -c --diff pure_protobuf tests

.PHONY: lint/mypy
lint/mypy:
	$(BIN)/mypy pure_protobuf tests

.PHONY: lint/format
lint/format:
	$(BIN)/black --check --diff pure_protobuf tests
