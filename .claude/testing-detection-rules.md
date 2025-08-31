# Testing Approach Detection Rules

This document defines the rules Claude Code uses to automatically determine the appropriate testing approach for a feature.

## Detection Priority

1. **Explicit Indicators** (highest priority)
2. **JIRA Issue Content**
3. **File Patterns**
4. **Technology Stack**
5. **Existing Test Patterns** (lowest priority)

## UI Testing Indicators

### Strong Indicators (use UI testing)
- JIRA issue contains keywords: "UI", "user interface", "button", "form", "page", "screen", "click", "navigate", "responsive", "mobile view", "desktop view"
- Acceptance criteria mentions: "user should see", "user clicks", "display", "show", "hide", "modal", "dropdown"
- File changes in: `/components/`, `/pages/`, `/views/`, `/frontend/`, `/client/`, `/app/`
- File extensions: `.jsx`, `.tsx`, `.vue`, `.svelte`, `.html`, `.css`, `.scss`

### Technology Indicators
- React/Vue/Angular/Svelte components
- CSS/SCSS/styled-components changes
- HTML templates
- Client-side routing files

## Backend API Testing Indicators (PyTest)

### Strong Indicators (use pytest)
- JIRA issue contains keywords: "API", "endpoint", "REST", "HTTP", "validation", "request", "response", "CRUD"
- File changes in: `/api/`, `/backend/`, `/routers/`, `/endpoints/`, `/controllers/`, `/views/`
- Files contain: `@app.route`, `@router`, `@api_view`, FastAPI/Flask/Django decorators
- NOT an MCP server (no @mcp_server decorators)

### Technology Indicators
- FastAPI, Flask, or Django REST in requirements.txt
- Existing pytest tests in tests/ directory
- TestClient or httpx usage
- OpenAPI/Swagger documentation

## MCP Testing Indicators

### Strong Indicators (use MCP testing)
- JIRA issue contains keywords: "MCP tool", "integration", "Conduit", "Claude subprocess"
- File changes in: `/mcp/`, `/tools/`
- Files contain: `@mcp_server.tool`, `FastMCP`, MCP-related imports
- Project identified as MCP server in server.py

### Technology Indicators
- Python files with MCP decorators specifically
- MCP server configuration
- Integration with external services via MCP

## Hybrid Testing Indicators

### Use Both Approaches When:
- JIRA issue mentions "end-to-end" or "full-stack"
- Changes span both `/frontend/` and `/backend/` directories
- Feature involves API + UI (e.g., "form that submits to API")
- Acceptance criteria includes both user actions AND system behavior

## Special Cases

### GraphQL APIs
- If mutations/queries + UI components → Hybrid
- If only GraphQL schema → MCP testing

### Static Sites
- If content changes only → Skip automated testing
- If interactive features → UI testing

### CLI Tools
- Command-line interfaces → MCP testing
- Web-based CLI → UI testing

### Mobile Apps
- React Native/Flutter → UI testing with specific mobile considerations
- Native mobile → Suggest platform-specific testing

## Decision Flow

```
1. Parse JIRA issue for keywords
2. Analyze file changes in current branch
3. Check technology stack
4. Look for existing test patterns
5. Make decision:
   - Strong UI indicators → UI Testing (Puppeteer)
   - Strong backend API indicators + no MCP → API Testing (PyTest)
   - Strong MCP indicators → MCP Testing (Claude subprocess)
   - Mixed indicators → Hybrid Testing (multiple approaches)
   - Unclear → Analyze acceptance criteria in detail
   - Still unclear → Ask user for guidance
```

## Testing Priority

When multiple approaches could apply:
1. MCP testing takes precedence if MCP decorators are found
2. API testing for standard REST endpoints without MCP
3. UI testing for frontend changes
4. Hybrid when changes span multiple layers

## Override Mechanisms

Users can override detection by:
1. Using specific commands: `/project:test-ui` or `/project:test-mcp`
2. Adding hints: `/project:test-issue ui-focused` or `/project:test-issue api-only`
3. Including testing approach in JIRA issue description

## Continuous Learning

Claude should note when detection was incorrect and adjust approach for similar issues in the future within the session.