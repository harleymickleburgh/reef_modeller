#!/bin/sh

.PHONY: test unit regression

test: unit regression

regression:
	@echo ">>> Running regression tests..."
	python3 -m unittest discover --start-directory=regression --pattern=test_*.py --verbose

unit:
	@echo ">>> Running unit tests..."
	python3 -m unittest discover --start-directory=. --pattern=*.py --verbose

