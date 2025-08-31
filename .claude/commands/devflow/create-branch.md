---
description: Create a branch for the JIRA issue and update its status
argument-hint: "[ISSUE-KEY] [SITE-ALIAS]"
allowed-tools: ["Bash", "mcp__Conduit__update_jira_status", "mcp__mcp_jira__update_jira_issue"]
---

## Create Branch and Update Status - FileOrbit Development

I'll create an appropriate Git branch for FileOrbit development and update the JIRA issue status to "In Progress".

## Grounding References
- **Branch Conventions**: Follow FileOrbit's feature/CP-XX-description naming pattern
- **Architecture Impact**: Check if changes affect distributed components (orchestrator/agents)

### Step 1: Determine Branch Type
Based on the issue type and FileOrbit conventions:
- **Feature/Story/Task**: `feature/CP-XX-<description>`
- **Bug**: `fix/CP-XX-<description>`
- **Hotfix**: `hotfix/CP-XX-<description>`

Note: FileOrbit uses CP-XX format for all JIRA issues

### Step 2: Create Branch
Create and checkout the new branch with appropriate naming.

### Step 3: Update JIRA Status
Update the issue status to "In Progress" using the provided site alias.

### Step 4: Confirm
Report the new branch name and confirm JIRA status update.

---

## ⛔ STOP HERE - Branch Created

**I have created the branch and updated JIRA. I will NOT proceed to planning.**

## 🔄 Next Step (For YOU to Run)

Now that you're on a development branch, YOU must run:

```
/project:devflow/plan-implementation
```

This will:
- Research any unfamiliar technologies
- Create a detailed implementation plan
- Prepare for exit plan mode

**DO NOT CONTINUE** - The user must explicitly run the next command.