# Test Structure

This directory contains all tests for the Voice Task Manager project, organized by type:

## Directory Structure

```
tests/
├── unit/                    # Unit tests for individual services
│   ├── test_task_manager.py
│   └── test_task_matcher.py
├── integration/             # Integration tests for service interactions
│   └── test_task_services.py
├── ui/                      # UI tests using Playwright (empty - see note below)
└── README.md               # This file
```

## Test Types

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions and classes in isolation
- **Scope**: Single service/component
- **Speed**: Fast
- **Dependencies**: Minimal (mocked where needed)
- **Examples**: TaskManager methods, TaskMatcher algorithms

### Integration Tests (`tests/integration/`)
- **Purpose**: Test interactions between multiple services
- **Scope**: Service-to-service communication
- **Speed**: Medium
- **Dependencies**: May require API keys (marked with `@pytest.mark.api`)
- **Examples**: CommandRouter with LLMService, data persistence

### UI Tests (`test_ui.py` in project root)
- **Purpose**: Test the Streamlit user interface
- **Scope**: End-to-end user interactions
- **Speed**: Slow (requires browser)
- **Dependencies**: Playwright, Streamlit app running
- **Examples**: Mode switching, button clicks, page loading
- **Note**: UI test file is kept at root level to avoid import path issues

## Running Tests

### Using Makefile (Recommended)
```bash
# Run all tests
make test-all

# Run specific test types
make test-unit
make test-integration
make test-ui

# Run without UI tests
make test

# Install dependencies
make install-deps
```

### Using PyTest Directly
```bash
# Run all tests
pytest tests/ -v

# Run specific test types
pytest tests/unit/ -v
pytest tests/integration/ -v
python test_ui.py  # UI tests

# Run with markers
pytest -m unit -v
pytest -m integration -v
pytest -m ui -v
pytest -m api -v  # Tests requiring API keys
```

## Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.ui` - UI tests
- `@pytest.mark.api` - Tests requiring API keys
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.asyncio` - Async tests

## Test Configuration

- **PyTest Config**: `pytest.ini` in project root
- **Test Discovery**: Automatically finds `test_*.py` files
- **Verbose Output**: Enabled by default
- **Markers**: Strict marker validation enabled

## Dependencies

### Required
- `pytest` - Test framework
- `pytest-asyncio` - Async test support

### Optional
- `playwright` - UI testing (for UI tests)
- `pytest-cov` - Coverage reporting

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Test names should clearly describe what they test
3. **Proper Assertions**: Use specific assertions with helpful error messages
4. **Mock External Dependencies**: Don't rely on external services in unit tests
5. **Clean Up**: Always clean up test data and resources
6. **Mark API Tests**: Use `@pytest.mark.api` for tests requiring API keys

## Adding New Tests

1. **Unit Tests**: Add to `tests/unit/` with descriptive filename
2. **Integration Tests**: Add to `tests/integration/` for service interactions
3. **UI Tests**: Add to `test_ui.py` in project root for interface testing
4. **Use Appropriate Markers**: Mark tests with relevant pytest markers
5. **Follow Naming Convention**: `test_*.py` for files, `test_*` for functions

## Troubleshooting

### UI Tests Not Running
- Ensure Playwright is installed: `playwright install`
- Check that Streamlit app can start on port 8501
- Verify browser dependencies are available

### Integration Tests Skipped
- Check for required API keys in environment
- Tests marked with `@pytest.mark.api` will be skipped without API keys

### Test Failures
- Run with `-v` for verbose output
- Use `--tb=short` for shorter tracebacks
- Check test isolation and cleanup 