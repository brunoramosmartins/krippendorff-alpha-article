.PHONY: install test lint docs docs-serve experiments clean

PYTHON ?= python
PIP ?= pip

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests/ -q

lint:
	$(PYTHON) -m ruff check src tests scripts

docs:
	$(PYTHON) -m mkdocs build --strict

docs-serve:
	$(PYTHON) -m mkdocs serve

# Phase 4: implement scripts and uncomment invocations below
experiments:
	@echo "Experiments are stubs until Phase 4. Then run:"
	@echo "  $(PYTHON) scripts/experiment_a_random.py"
	@echo "  $(PYTHON) scripts/experiment_b_trap.py"
	@echo "  $(PYTHON) scripts/experiment_c_llm.py"
	@echo "  $(PYTHON) scripts/experiment_d_missing.py"

clean:
	rm -rf site/ .pytest_cache .ruff_cache **/__pycache__
	@echo "On Windows PowerShell you can use: Remove-Item -Recurse -Force site -ErrorAction SilentlyContinue"
