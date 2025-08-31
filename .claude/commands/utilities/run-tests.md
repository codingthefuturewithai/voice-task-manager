---
description: Run project-specific tests and quality checks
argument-hint: "[TEST-TYPE]"
allowed-tools: ["Bash", "Read"]
---

Running tests for the Conduit project.

## Test Execution Plan

Based on the argument "$ARGUMENTS", I'll run:

### All Tests (default)
!pytest
!ruff check .
!black --check .
!mypy .

### Unit Tests Only
!pytest tests/unit/

### Integration Tests Only  
!pytest tests/integration/

### MCP Tests Only
!pytest tests/mcp/

### Quick Tests (fast feedback)
!pytest -x --ff
!ruff check .

### Coverage Report
!pytest --cov=conduit --cov-report=html

I'll provide a summary of the results after the tests complete.