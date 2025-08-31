---
description: Complete the issue with PR creation and JIRA update
argument-hint: "[SITE-ALIAS]"
allowed-tools: ["Bash", "mcp__Conduit__update_jira_status", "mcp__mcp_jira__update_jira_issue"]
---

## Complete Issue and Create PR - FileOrbit Development

I'll finalize your implementation, create a pull request, and update JIRA.

## Parse Arguments
- Site alias provided: $ARGUMENTS (e.g., "fileorbit")
- I'll extract the JIRA issue key from the current branch name (feature/CP-XX-description)

### Step 1: Run Final Quality Checks
Ensure code quality before creating PR:

!ruff check . # Python linting
!ruff format --check . # Python formatting
!pytest # Backend tests
# Future: ESLint for TypeScript when configured

**IMPORTANT**: If any of these checks fail:
- **Python linting**: Fix with `ruff check --fix .` or manually
- **Python formatting**: Fix with `ruff format .`
- **Test failures**: Return to implementation to fix issues
- **Docker builds**: Verify containers build if affected
- Do NOT proceed until all checks pass!

### Step 2: Stage and Commit Changes
I'll create a comprehensive commit with:
- Conventional commit format based on issue type
- Detailed description of changes
- JIRA issue reference
- Claude Code attribution

!git add -A

### Step 3: Push Branch
Push the feature branch to remote:

!git push -u origin $(git branch --show-current)

### Step 4: Create Pull Request
First, verify GitHub CLI is available:
!gh --version

If `gh` is not installed:
- macOS: `brew install gh`
- Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
- Then run: `gh auth login`

Create PR using GitHub CLI with:
- Clear title referencing CP-XX issue
- Summary of changes and affected components (backend/frontend/agent)
- Test plan including any Docker/distributed testing
- Impact on FileOrbit architecture noted
- Claude Code attribution

### Step 5: Update JIRA Status
Update the issue to "Done" and add PR link as comment.

---

## ⛔ STOP HERE - PR Created

**I have created the PR and updated JIRA. I will NOT proceed further.**

## 🔄 Next Step (For YOU to Run AFTER PR is Merged)

After your PR is reviewed and merged by a team member, YOU must run:

```
/project:devflow/post-merge
```

This will:
- Sync your local main with remote
- Clean up the feature branch
- Prepare for your next issue

**DO NOT CONTINUE** - Wait for PR review and merge, then run post-merge command.