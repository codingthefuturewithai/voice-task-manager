---
description: Research and create implementation plan ONLY - does NOT implement code
argument-hint: ""
allowed-tools: ["mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "WebSearch", "Read", "ExitPlanMode"]
---

## Plan Implementation - FileOrbit Development

⚠️ **CRITICAL COMMAND BOUNDARY** ⚠️
- This command MUST ONLY create plans
- This command MUST NOT write any code
- This command MUST NOT implement anything
- This command MUST NOT use Write, Edit, or MultiEdit tools
- Even if the user says "approved" or "looks good", DO NOT IMPLEMENT

I'll create a detailed implementation plan for FileOrbit based on the JIRA issue requirements.

## Grounding References - FileOrbit Architecture
- **System Architecture**: `.reference/fileorbit-architecture.md` - Core system design
- **Critical Files**: `.reference/critical-files.md` - What not to break
- **Distributed Systems**: `.reference/distributed-architecture.md` - Orchestrator and agent patterns

## Grounding References - FileOrbit Components
- **Backend Patterns**: FastAPI with async patterns for job processing
- **Frontend Patterns**: React + TypeScript + Mantine UI components
- **Agent Patterns**: Distributed agents with gRPC and RabbitMQ integration
- **Database Models**: SQLAlchemy models for PostgreSQL
- **Job Processing**: Redis queue with rclone subprocess management

### Step 1: Technical Research
If the issue mentions unfamiliar technologies:
- Use Context7 for library/framework documentation
- Research best practices for the specific technology
- Note any special setup requirements

### Step 2: Identify Components
Based on requirements and existing FileOrbit code:
- Backend files to modify (backend/)
- Frontend components to update (frontend/)
- Agent services to modify (agent/)
- Database models or migrations needed
- API endpoints to add/modify
- Integration points with orchestrator/agents

### Step 3: Define Testing Strategy
Determine the appropriate testing approach:
- **Frontend Testing**: React components with potential Vitest/Jest
- **Backend Testing**: FastAPI endpoints with pytest
- **Agent Testing**: gRPC services and RabbitMQ integration
- **Integration Testing**: End-to-end workflow testing
- **Unit Testing**: Individual functions and utilities

### Step 4: Create Implementation Plan
Present a structured plan with:
1. Overview of approach
2. Implementation order
3. Components to build/modify (backend/frontend/agent)
4. Testing strategy (pytest for backend, vitest for frontend)
5. Risk factors or dependencies
6. Impact on distributed architecture

**Key Patterns to Follow**:
- FastAPI async patterns for backend endpoints
- React functional components with hooks
- gRPC async patterns for agent communication
- RabbitMQ message handling patterns
- Database session management with SQLAlchemy

### Step 5: Present Plan and STOP COMPLETELY
I'll use ExitPlanMode to present the complete plan for your review.

**THEN I MUST STOP. NO FURTHER ACTION.**

---

## 🛑 FULL STOP - Plan Presented

**THIS COMMAND ENDS HERE. I WILL NOT IMPLEMENT ANYTHING.**

After the plan is presented:
1. **You review the plan** 
2. **You decide** what to do next

## 🔄 What YOU Must Do Next

**To implement the plan**, YOU must explicitly run:
```
/project:devflow/implement-plan
```

**To revise the plan**:
- Tell me what needs to be different
- I'll revise the plan (still no implementation)
- We stay in planning mode only

**CRITICAL RULES**:
- Even if you say "approved" → I MUST NOT implement
- Even if you say "looks good" → I MUST NOT implement  
- Even if you say "go ahead" → I MUST NOT implement
- ONLY the command `/project:devflow/implement-plan` can trigger implementation

**No code will be written by this command under ANY circumstances.**