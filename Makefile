# SoftCropper Makefile

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $(VENV)/bin/pytest

.PHONY: all venv install test clean build

all: test

venv:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip

install: venv
	@$(PIP) install -e .
	@$(PIP) install pytest

test: install
	@$(PYTEST) tests -v

build:
	@rm -rf dist
	@$(PYTHON) setup.py sdist bdist_wheel

clean:
	@rm -rf $(VENV) dist *.egg-info __pycache__ .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@find . -type d -name "*.egg-info" -exec rm -r {} +
