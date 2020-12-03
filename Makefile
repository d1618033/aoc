FOLDERS:=aoc tests

do_format:
	isort $(FOLDERS)
	black $(FOLDERS)

format:
	isort -c $(FOLDERS)
	black -c $(FOLDERS)

test:
	pytest -s -vvv tests

test_day%:
	pytest -s -vvv tests/day$*

lint:
	pylint $(FOLDERS)
	flake8 $(FOLDERS)
	mypy $(FOLDERS)
