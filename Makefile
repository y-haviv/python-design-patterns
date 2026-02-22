.PHONY: help install install-dev format lint type-check test coverage clean all

help:
	@echo "Python Design Patterns - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install dependencies"
	@echo "  make install-dev      - Install dev dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format           - Format code with black and isort"
	@echo "  make lint             - Run flake8 linting"
	@echo "  make type-check       - Run mypy type checking"
	@echo "  make check            - Run all quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run tests"
	@echo "  make coverage         - Run tests with coverage report"
	@echo "  make coverage-html    - Generate HTML coverage report"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit       - Run pre-commit hooks"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove generated files"
	@echo "  make clean-all        - Remove all generated files and cache"
	@echo ""
	@echo "Meta:"
	@echo "  make help             - Show this help message"
	@echo "  make all              - Run all checks and tests"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install black isort flake8 mypy pytest-cov pre-commit

format:
	@echo "Formatting code with black and isort..."
	black .
	isort .
	@echo "Done!"

lint:
	@echo "Running flake8..."
	flake8 .

type-check:
	@echo "Running mypy type checking..."
	mypy .

check: format lint type-check
	@echo "All quality checks passed!"

test:
	pytest -v

test-fast:
	pytest -v --tb=short

coverage:
	pytest --cov=. --cov-report=term-missing

coverage-html:
	pytest --cov=. --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

pre-commit:
	pre-commit run --all-files

clean:
	@echo "Cleaning generated files..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.mypy_cache' -delete
	rm -rf dist/ build/
	@echo "Done!"

clean-all: clean
	@echo "Cleaning all generated files..."
	rm -rf .tox/ .coverage htmlcov/
	find . -type d -name '.venv' -o -name 'venv' -prune
	@echo "Done!"

all: install-dev format lint type-check test coverage
	@echo ""
	@echo "✓ All checks and tests passed successfully!"
