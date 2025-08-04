.PHONY: test test-unit test-integration test-ui test-all clean help

# Default target
help:
	@echo "Available commands:"
	@echo "  test-all        - Run all tests (unit, integration, UI)"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-ui         - Run UI tests only"
	@echo "  test            - Run unit and integration tests (no UI)"
	@echo "  clean           - Clean up test artifacts"
	@echo "  install-deps    - Install test dependencies"

# Install test dependencies
install-deps:
	pip install pytest pytest-asyncio playwright
	playwright install

# Run all tests
test-all: test test-ui

# Run unit and integration tests (no UI)
test:
	pytest tests/unit/ tests/integration/ -v

# Run unit tests only
test-unit:
	pytest tests/unit/ -v

# Run integration tests only
test-integration:
	pytest tests/integration/ -v

# Run UI tests only
test-ui:
	python test_ui.py

# Run tests with coverage
test-coverage:
	pytest tests/unit/ tests/integration/ --cov=services --cov-report=html --cov-report=term

# Clean up test artifacts
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage 