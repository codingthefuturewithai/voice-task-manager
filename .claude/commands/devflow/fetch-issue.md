---
description: Fetch and understand a JIRA issue for FileOrbit development
argument-hint: "[ISSUE-KEY] [SITE-ALIAS]"
allowed-tools: ["mcp__Conduit__search_jira_issues", "mcp__mcp_jira__search_jira_issues"]
---

## Fetch JIRA Issue - FileOrbit Development

I'll fetch and summarize JIRA issue $ARGUMENTS for FileOrbit development work.

## Grounding References
- **Project Context**: Working on FileOrbit - enterprise UI layer for rclone with distributed architecture
- **Architecture Guide**: See `.reference/fileorbit-architecture.md` and CLAUDE.md for system overview

### Step 1: Parse Arguments
- Arguments: $ARGUMENTS
- Expected format: [ISSUE-KEY] [SITE-ALIAS] (e.g., "CP-123 fileorbit")

### Step 2: Fetch Issue Details
Using the parsed issue key and site alias to retrieve the issue from JIRA.

### Step 3: Summary
After fetching, I'll provide:
- **Issue Type**: (Bug/Feature/Task/Story)
- **Summary**: Brief description
- **Status**: Current workflow state
- **Key Requirements**: What needs to be done
- **Acceptance Criteria**: How we'll know it's complete
- **Priority**: Issue priority level
- **Assignee**: Who's responsible

---

## ⛔ STOP HERE - Command Complete

**I have fetched and summarized the issue. I will NOT proceed further.**

## 🔄 Next Step (For YOU to Run)

To analyze if this issue is already implemented, YOU must run:

```
/project:devflow/analyze-feasibility
```

**DO NOT CONTINUE** - The user must explicitly run the next command.