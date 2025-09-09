---
description: Discover and document all user interface elements and their capabilities in this repository
argument-hint: "[--visual-verification]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "MultiEdit", "Bash", "mcp__playwright__*", "Task"]
---

## Discover UI Elements and Capabilities

I need to understand what user interface elements exist in this repository and what they can actually do.

The results will be saved to `.reference/ui_elements.json` in the repository root.

### Discovery Process

#### 1. Understand What This Repository Is
Let the code reveal itself:
- What files and directories exist?
- What programming languages are present?
- What entry points or main files can I identify?
- What dependencies or libraries are being used?

#### 2. Find User Interface Elements
Without assuming any specific technology:
- Locate code that renders or displays things to users
- Identify code that accepts user input
- Find interactive elements (things users can click, type into, select, etc.)
- Discover what creates visual output

#### 3. Trace Interaction Capabilities
For each interactive element discovered:
- What happens when a user interacts with it?
- Follow the code path from interaction to outcome
- What data or state gets modified?
- What functions or methods are invoked?
- What are the actual limits of what can be changed?

#### 4. Map Modification Workflows
For any data that can be modified:
- How can users modify it through the interface?
- What fields/properties are actually editable?
- What modification paths exist?
- What requires alternative approaches and why?

#### 5. Document Behavioral Truth
Create a comprehensive map showing:
- Every interactive element found
- What each element can actually do (not what it appears to do)
- The real workflows for accomplishing tasks
- Limitations discovered through code analysis
- Why certain operations work the way they do

### Analysis Method

Start from entry points and follow the code:
1. Find main/entry files by looking for execution patterns
2. Trace from user interface elements to backend logic
3. Map the complete interaction flow for each element
4. Verify what's actually possible versus what appears possible

### Special Focus Areas

When analyzing modification capabilities:
- Can existing data be edited? Which fields?
- What triggers edit modes or states?
- What gets saved when users confirm changes?
- What's the difference between what's shown and what's editable?

### Output

The analysis will be saved to `.reference/ui_elements.json`:
- If the file exists, it will be updated with the new analysis
- If the file doesn't exist, it will be created
- The `.reference` directory will be created if it doesn't exist

The JSON structure will capture:
- All interactive elements discovered
- Their actual capabilities (based on code, not assumptions)
- Workflows for user operations
- Limitations and constraints
- The "why" behind any restrictions

### Visual Verification (if --visual-verification flag is provided)

If requested and appropriate tools are available:
1. Launch the application
2. Interact with discovered elements
3. Verify the code analysis findings
4. Document any discrepancies between code and behavior

---

## Important Notes

- Make no assumptions about technology stack
- Let the code patterns reveal what framework/library is used
- Discover capabilities through code analysis, not expectations
- Document what IS possible, not what SHOULD BE possible
- Focus on behavioral truth derived from the actual implementation