---
description: Run tests created during implementation to validate changes
argument-hint: "[OPTIONAL-HINTS]"
allowed-tools: ["Bash", "Read", "Grep", "Task"]
---

## Run Tests for Current Implementation - FileOrbit Development

I'll run the tests that were created during the implementation phase to validate all changes work correctly.

## Grounding References
- **Backend Testing**: pytest for FastAPI endpoints and async operations
- **Frontend Testing**: Future Vitest setup for React components
- **Agent Testing**: Integration tests for gRPC and RabbitMQ

### Step 1: Verify Tests Exist
Check that tests were created during implementation:
- Look for new test files in `tests/` directory
- Confirm test coverage for new functionality
- If tests are missing, return to `implement-plan` to add them

### Step 2: Run Tests
Execute the appropriate test suites:
- **Backend Tests**: `pytest backend/tests/ -v`
- **Agent Tests**: `pytest agent/tests/ -v` (if exists)
- **Full Suite**: `pytest -v`
- **With Coverage**: `pytest --cov=backend --cov-report=term-missing`
- **Docker Tests**: Test services in containers if needed

### Step 3: Fix Failures
If any tests fail:
- Analyze the failure reason
- Fix implementation or test as needed
- Re-run tests to confirm fixes

### Step 4: Validate Coverage
Ensure adequate test coverage:
- New backend code should have >80% coverage
- Critical paths (job processing, data transfers) should have 100% coverage
- Error cases and async operations must be tested
- Integration points with orchestrator/agents must be validated

---

## ⛔ STOP HERE - Testing Complete

**I have run the tests. I will NOT proceed to creating a PR.**

## 🔄 Next Step (For YOU to Run)

After tests pass successfully, YOU must run:

```
/project:devflow/complete-issue [SITE-ALIAS]
```

This will:
- Create a pull request with your changes
- Update JIRA status to Done
- Provide PR link for review

**DO NOT CONTINUE** - The user must explicitly run the complete command.