FOLDERS:=aoc tests

do_format:
	isort $(FOLDERS)
	black $(FOLDERS)

format:
	black -c $(FOLDERS)

test:
	pytest -s -vvv tests

test_day%:
	pytest -s -vvv tests/day$*

pylint:
	pylint $(FOLDERS)

flake8:
	flake8 $(FOLDERS)

mypy:
	MYPYPATH=stubs mypy $(FOLDERS)

lint: flake8 pylint mypy

check: format lint test
