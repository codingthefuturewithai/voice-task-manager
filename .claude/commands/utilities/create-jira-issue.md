---
description: Create a detailed JIRA issue by analyzing the codebase and structuring it according to team standards
argument-hint: "\"[description of the issue or feature]\""
allowed-tools: ["Read", "Grep", "Task", "mcp__Conduit__create_jira_issue", "mcp__mcp_jira__create_jira_issue"]
---

# Create JIRA Issue

I'll help you create a detailed JIRA issue by analyzing the codebase and structuring it according to team standards.

## Understanding Your Request

You said: "$ARGUMENTS"

Let me gather the required information from you first.

## Step 1: Get Required Information

Based on your description, I think this might be a **[Executable Spec/Bug/Task]** - but let me confirm with you.

**1. Which JIRA site should I use?** 
Please specify the site alias (you have multiple configured).

[WAIT for user response - DO NOT PROCEED without this]

**2. Which JIRA project should this go in?** 
(e.g., ASEP, DEV, PROJ)

[WAIT for user response - DO NOT PROCEED without this]

**3. What type of issue is this?**
- Executable Spec (new feature/capability)
- Bug (something is broken)
- Task (maintenance/improvement)

I think it's a [inferred type] based on your description, but please confirm.

[WAIT for user response - DO NOT PROCEED without this]

**4. What should the title be?**
Based on your description, I suggest: "[proposed title]"
Is this good or would you like to change it?

[WAIT for user response - DO NOT PROCEED without this]

## Step 2: Analyze Codebase Context

Now let me analyze the codebase to understand the context better...

[Perform relevant searches based on the issue description]

Based on my analysis, I found:
- Related components: [list findings]
- Similar patterns: [list patterns]
- Potential impact areas: [list areas]

## Step 3: Structure the Issue

Based on your requirements and my analysis, here's the JIRA issue I'll create:

**Site**: [user-provided site alias]
**Project**: [user-provided project key]
**Type**: [user-confirmed type]
**Title**: [user-approved title]

### Description:

[Show the complete formatted description based on type]

#### For Executable Spec:
**Background/Goal**
- [Context from codebase analysis]
- [Problem this solves]
- [Value delivered]

**Acceptance Criteria**
1. [Specific, testable requirement]
2. [Another requirement]
3. [etc.]

**Technical Approach**
- [Implementation guidance based on codebase patterns]
- [Files/components to modify]
- [Integration points]

**Testing Requirements**
- [Unit test coverage needed]
- [Integration test scenarios]

#### For Bug:
**Problem Statement**
[Clear description of what's broken]

**Steps to Reproduce**
1. [Step 1]
2. [Step 2]
3. [Expected vs Actual]

**Root Cause**
[Based on codebase analysis]

**Proposed Solution**
[Technical approach to fix]

**Testing Requirements**
- [How to verify fix]
- [Regression tests needed]

---

## Step 4: Review and Confirm

**⚠️ IMPORTANT: Please review the issue above carefully.**

Is this ready to create? 
- **Yes** - Create the issue as shown
- **Edit** - Tell me what to change
- **Cancel** - Don't create the issue

[WAIT for EXPLICIT user confirmation - NEVER create without "Yes" or explicit approval]

## Step 5: Create the Issue (ONLY after explicit approval)

[Only proceed here if user explicitly said "Yes" or "Create it" or similar approval]

Creating JIRA issue with:
- Site: [confirmed site]
- Project: [confirmed project]
- Type: [confirmed type]
- Summary: [confirmed title]
- Description: [confirmed description]

[Use mcp__mcp_jira__create_jira_issue if available, otherwise fall back to mcp__Conduit__create_jira_issue]

[Prefer mcp__mcp_jira__create_jira_issue as it's the dedicated JIRA server with better formatting support]

✅ **Issue Created Successfully!**
- Issue Key: [PROJ-123]
- URL: [link to issue]
- Suggested branch name: `feature/PROJ-123-short-description`

**Next steps:**
1. Review the issue in JIRA
2. Add any additional details/attachments
3. Assign to appropriate team member
4. Begin implementation when ready

## ⚠️ CRITICAL RULES

**NEVER:**
- Create an issue without explicit user approval
- Assume which site to use
- Assume which project to use
- Create a title without user confirmation
- Skip any of the required information gathering steps

**ALWAYS:**
- Wait for user to provide site alias
- Wait for user to provide project key
- Wait for user to confirm issue type
- Wait for user to approve the title
- Show the complete issue for review
- Wait for explicit "Yes" or approval before creating