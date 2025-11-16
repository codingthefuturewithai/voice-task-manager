---
description: Check for .reference directory and either create it fresh or offer to recreate it
argument-hint: "[--force]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "MultiEdit", "Bash", "Task", "TodoWrite"]
---

## Initialize or Recreate Reference Directory

I'll check if the `.reference` directory exists and handle it appropriately.

### Step 1: Check for existing .reference directory

```bash
if [ -d ".reference" ]; then
    echo "📁 Found existing .reference directory with the following contents:"
    echo ""
    ls -la .reference/
    echo ""
    echo "Would you like to:"
    echo "1) Delete everything and recreate from scratch"
    echo "2) Cancel and keep existing content"
    echo ""
    echo "Please type 1 or 2:"

    # STOP HERE AND WAIT FOR USER RESPONSE
    # Do not proceed until user makes a choice
else
    echo "📂 No .reference directory found."
    echo "Proceeding to create it and analyze the codebase..."
    mkdir -p .reference

    # Only continue if directory didn't exist
    # Proceed with full codebase analysis below
fi
```

### If user chooses option 1 (recreate) or directory didn't exist:

```bash
# Only run this if user chose to recreate OR directory didn't exist
if [ "$USER_CHOICE" = "1" ] || [ "$DIRECTORY_DID_NOT_EXIST" = "true" ]; then
    # Clear if recreating
    if [ -d ".reference" ] && [ "$USER_CHOICE" = "1" ]; then
        echo "🗑️ Removing existing .reference contents..."
        rm -rf .reference/*
    fi

    echo "🚀 Starting fresh codebase analysis..."
fi
```

### Phase 2: Full Codebase Analysis (only if proceeding)

Now analyze the codebase and create all documentation files:

1. **Architecture Documentation** (`.reference/task-tracker-architecture.md`)
2. **Voice Commands Guide** (`.reference/voice-commands-guide.md`)
3. **User Workflows** (`.reference/user_workflows.md`)
4. **Getting Started Guide** (`.reference/getting-started-guide.md`)
5. **UI Elements Catalog** (`.reference/ui_elements.json`)

[Rest of analysis steps from refresh-knowledge command]

---

## Key Difference from refresh-knowledge

This command:
- **CHECKS FIRST** if .reference exists
- **ASKS YOU** what to do if it exists
- **WAITS** for your decision
- **ONLY PROCEEDS** if you say to recreate OR if directory doesn't exist

The refresh-knowledge command:
- **ASSUMES** .reference exists
- **IMMEDIATELY** starts updating
- **NEVER ASKS** for permission