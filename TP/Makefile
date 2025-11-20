test:
	coverage run -m pytest

unit_test:
	pytest -m "not perf"

perf_test:
	pytest -m perf

coverage:
	coverage report -m

lint:
	ruff check .

doc:
	pdoc3 --html --output-dir docs src/triangulator
