.PHONY: help install dev test test-cov lint format clean build upload upload-test

help:
	@echo "Available commands:"
	@echo "  install      Install package in development mode"
	@echo "  dev          Install development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting (flake8, mypy)"
	@echo "  format       Format code (black)"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI"
	@echo "  upload-test  Upload to Test PyPI"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=temp_mail_api --cov-report=html --cov-report=term-missing

lint:
	flake8 temp_mail_api tests examples
	mypy temp_mail_api

format:
	black temp_mail_api tests examples

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

upload-test: build
	python -m twine upload --repository testpypi dist/* 