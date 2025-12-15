.PHONY: test unit_test perf_test coverage lint doc

test:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && coverage run -m pytest

unit_test:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && pytest -m "not perf"

perf_test:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && pytest -m perf -v -s

coverage:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && coverage report -m

lint:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && ruff check .

doc:
	cd /Users/thaha/Documents/cours/M1/techniques_de_test/techniques_de_test_2025_2026/TP && pdoc3 --html --output-dir docs src/triangulator --force
