---
description: Implement the approved plan - actual coding phase
argument-hint: ""
allowed-tools: ["Read", "Write", "Edit", "MultiEdit", "Bash", "Grep", "Glob", "TodoWrite"]
---

## Implement Approved Plan - FileOrbit Development

I'll now implement the plan that was previously created and approved.

## Prerequisites
This command should only be run after:
1. `/project:devflow/plan-implementation` has been executed
2. You have reviewed and approved the plan

## Grounding References for Implementation
- **Architecture Guide**: `.reference/fileorbit-architecture.md`
- **Critical Files**: `.reference/critical-files.md`
- **Distributed Systems**: `.reference/distributed-architecture.md`
- **Backend Patterns**: FastAPI async patterns with SQLAlchemy
- **Frontend Patterns**: React + TypeScript + Mantine UI
- **Agent Patterns**: gRPC services with RabbitMQ integration

## Implementation Process

### Step 1: Review Plan
I'll reference the plan created earlier to ensure alignment.

### Step 2: Implement Changes
Following the approved plan, I'll:
- Create new files as specified
- Modify existing files according to requirements  
- Apply FileOrbit patterns and conventions
- Follow architecture guidelines from `.reference/`
- Ensure distributed system compatibility

### Step 3: Generate Tests
**CRITICAL**: Tests must be created alongside implementation:

**Test Requirements by Component Type:**
- **For Backend APIs**: Create pytest tests for FastAPI endpoints
- **For Frontend Components**: Create component tests (future Vitest setup)
- **For Agent Services**: Create integration tests for gRPC and RabbitMQ
- **For Database Models**: Create SQLAlchemy model tests
- **For Job Processing**: Create async job execution tests

**Special Rules:**
- If JIRA affects distributed components → Test orchestrator/agent communication
- If implementing new protocols → Test all protocol handlers
- If modifying job processing → Test async execution and error handling
- Backend tests use pytest with async support
- Tests should validate both success and error cases
- Test database operations with proper session management

**Example**: New transfer protocol requires:
1. Protocol handler unit tests
2. Integration tests with agent communication
3. End-to-end transfer workflow tests

### Step 4: Track Progress
I'll use TodoWrite to track implementation tasks as I complete them.

### Step 5: Verify Implementation
After each major component:
- Ensure code follows patterns
- Check decorator requirements
- Validate async/await usage
- Confirm Context parameter inclusion
- Confirm tests are created and follow patterns

### Step 6: Run Linting and Formatting
Before moving to testing, ensure code quality:
- **Python**: Run `ruff check .` and `ruff format .`
- **TypeScript**: Run ESLint for frontend code (when configured)
- Fix any remaining linting errors
- Ensure all files follow FileOrbit code style
- Check Docker builds if containers are affected

---

## ⛔ STOP HERE - Implementation Complete

**I have implemented the approved plan. I will NOT proceed to testing.**

## 🔄 Next Step (For YOU to Run)

After implementation is complete, YOU must run:

```
/project:devflow/test-issue
```

This will:
- Analyze what was implemented
- Run appropriate tests
- Validate the implementation meets requirements

**DO NOT CONTINUE** - The user must explicitly run the test command.