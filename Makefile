SHELL := /bin/bash

# --- Configurable knobs ---
PY ?= python3
PIP := $(PY) -m pip
VENV := .venv
ACT := source $(VENV)/bin/activate
PKG ?= chatbot
TESTS ?= tests

.DEFAULT_GOAL := help

# --- Environments & installs ---
venv:
	@test -d $(VENV) || $(PY) -m venv $(VENV)
	@$(ACT) && $(PIP) install --upgrade pip

install: venv
	@$(ACT) && $(PIP) install -r requirements.txt

dev: install
	@$(ACT) && $(PIP) install -r requirements-dev.txt
	@$(ACT) && pre-commit install

precommit:
	@$(ACT) && pre-commit run --all-files

# --- Quality gates ---
format:
	@$(ACT) && ruff check . --fix
	@$(ACT) && black .

lint:
	@$(ACT) && ruff check .
	@$(ACT) && black --check .

typecheck:
	@$(ACT) && mypy $(PKG)

# --- Tests ---
test:
	@$(ACT) && pytest -q

cov:
	@$(ACT) && pytest -q --cov=$(PKG) --cov-report=term-missing

cov-html:
	@$(ACT) && pytest -q --cov=$(PKG) --cov-report=html && \
	echo 'Open: htmlcov/index.html'

# --- Run app ---
run:
	@$(ACT) && $(PY) main.py

# --- Utilities ---
env:
	@if [ ! -f .env ] && [ -f .env.example ]; then cp .env.example .env; \
	echo 'Created .env from .env.example'; else \
	echo '.env already present or .env.example missing'; fi

ci: lint typecheck cov

clean:
	@rm -rf __pycache__ */__pycache__ .pytest_cache .mypy_cache .ruff_cache \
	.coverage htmlcov .tox dist build

help:
	@echo 'Targets:'
	@echo '  venv           - create virtualenv and upgrade pip'
	@echo '  install        - install runtime deps'
	@echo '  dev            - install runtime + dev deps and pre-commit hook'
	@echo '  precommit      - run pre-commit on all files'
	@echo '  format         - auto-fix style (ruff+black)'
	@echo '  lint           - lint & format check (no changes)'
	@echo '  typecheck      - static types via mypy'
	@echo '  test           - run pytest'
	@echo '  cov            - run pytest with coverage summary'
	@echo '  cov-html       - generate HTML coverage report'
	@echo '  run            - run the app (main.py)'
	@echo '  env            - create .env from .env.example if missing'
	@echo '  ci             - lint + typecheck + coverage (for CI parity)'
	@echo '  clean          - remove caches & artifacts'

.PHONY: venv install dev precommit format lint typecheck test cov cov-html run env ci clean help
