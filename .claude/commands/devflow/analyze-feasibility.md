---
description: Analyze if a JIRA issue's requirements are already implemented
argument-hint: ""
allowed-tools: ["Grep", "Glob", "Read", "Task", "Bash"]
---

## Analyze Implementation Feasibility - FileOrbit

I'll analyze the FileOrbit codebase to determine if the JIRA issue's requirements are already implemented or if there are any conflicts.

## Grounding References
- **Critical Files**: Check `.reference/critical-files.md` before modifying core components
- **Architecture Guide**: See `.reference/fileorbit-architecture.md` for system overview
- **Distributed Systems**: Reference `.reference/distributed-architecture.md` for orchestrator/agent patterns

### Step 1: Extract Key Terms
From the previously fetched JIRA issue, I'll identify:
- Function/class names mentioned
- Feature keywords
- UI components or endpoints
- Configuration settings

### Step 2: Search Codebase
I'll search for existing implementations:
- Grep for relevant keywords and patterns
- Check backend/ (FastAPI), frontend/ (React), agent/ (distributed)
- Review recent commits for related work
- Look for feature flags, environment variables, or configuration
- Check orchestrator and agent services for distributed features

### Step 3: Check Documentation
- Search README and CLAUDE.md for feature mentions
- Look for architecture decisions in .reference/
- Check for deprecation notices
- Review distributed architecture documentation
- Check if feature affects orchestrator, agents, or API

### Step 4: Report Findings
I'll provide a clear assessment:
- **Not Implemented**: Ready to proceed ✅
- **Partially Implemented**: What exists vs. what's missing 🔄
- **Fully Implemented**: Evidence of existing implementation ❌
- **Conflicts Found**: Architectural concerns to discuss ⚠️

---

## ⛔ STOP HERE - Analysis Complete

**I have completed the feasibility analysis. I will NOT create a branch or take any other action.**

## 🔄 Next Steps (For YOU to Decide and Run)

Based on my findings above, YOU must decide what to do:

**If NOT implemented or PARTIALLY implemented, YOU run:**
```
/project:devflow/create-branch [ISSUE-KEY] [SITE-ALIAS]
```

**If FULLY implemented:**
Consider closing the JIRA issue or converting to documentation task.

**If CONFLICTS found:**
Discuss with team before proceeding.

**DO NOT CONTINUE** - The user must explicitly run the next command based on the analysis.