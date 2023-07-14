test:
	@echo ">>> Running tests..."
	cd tests && make && cd ..
	@echo "Done!"

clean:
	@echo ">>> Cleaning up..."
	cd doc && make clean && cd ..
	cd tests && make clean && cd ..
	python setup.py clean
	@echo "Done!"

lint:
	@echo "    Linting CoralODElab codebase"
	@python3 -m flake8 *.py
	@echo "    Linting CoralODElab test suite"
	cd test && python3 -m flake8 test && cd ..
