FOLDERS:=aoc tests

do_format:
	autoflake -i -r --remove-all-unused-imports $(FOLDERS)
	isort $(FOLDERS)
	black --target-version py310 $(FOLDERS) 

format:
	isort -c $(FOLDERS)
	black -c $(FOLDERS)

test:
	pytest -s -vvv tests

test_day:
	pytest -s -vvv tests/year$(YEAR)/test_day$(DAY).py

solve_day:
	aoc solve --year $(YEAR) --day $(DAY)

pylint:
	pylint $(FOLDERS)

flake8:
	flake8 $(FOLDERS)

mypy:
	MYPYPATH=stubs mypy $(FOLDERS)

lint: flake8 pylint mypy

check: format lint test
