---
description: Interactive guided tour of the Voice Task Manager - learn step by step based on your needs
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "Bash", "mcp__context7__resolve-library-id", "mcp__context7__get-library-docs", "WebSearch", "WebFetch"]
---

# Welcome to Voice Task Manager! 🎤

First, let me understand your setup:
```bash
pwd  # Check current directory
ls -la | head -5  # See project structure
```

Now I can see we're in the task-tracker - an AI-powered voice task management application. Let's get you started!

## Choose Your Learning Path

**What would you like to learn?**

1. **Understand the Architecture** - How does this voice task manager work internally?
2. **Learn the Features** - What can this app do with voice commands?
3. **Explore the Code** - Dive into the services and implementation
4. **Just Get Started** - Quick setup and first voice command

**Type 1, 2, 3, or 4** to choose what you'd like to explore.


## Note for AI Assistants - CRITICAL INSTRUCTIONS

### KNOWLEDGE BASE FIRST
Always read these .reference files BEFORE answering:
- `.reference/task-tracker-architecture.md` - System architecture
- `.reference/voice-commands-guide.md` - All voice commands
- `.reference/getting-started-guide.md` - Setup instructions
- `.reference/user_workflows.md` - UI workflows

### PATH SELECTION

Based on user's choice (1, 2, 3, or 4), follow the appropriate path:

#### Path 1: Understand the Architecture
1. Read `.reference/task-tracker-architecture.md` FIRST
2. Explain the architecture ONE concept at a time (keep each brief - 2-3 sentences):
   
   **Concept**: Voice-to-Task Pipeline
   - "Your voice goes through: Recording → Whisper (speech-to-text) → GPT-5 nano (understanding) → Task execution"
   - "The app has two modes: Brain Dump (multiple tasks) and Command (single actions)"
   - "Does this flow make sense?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Service Architecture
   - "The app uses 6 main services:"
   - "• WhisperService - Converts your speech to text"
   - "• LLMService - Understands what you want to do (uses GPT-5 nano)"
   - "• TaskManager - Stores and manages your tasks locally"
   - "• CommandRouter - Routes commands to the right handler"
   - "• TTSService - Provides voice feedback using browser speech"
   - "Clear so far?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Operating Modes
   - "Brain Dump Mode: Speak freely about multiple tasks"
   - "Example: 'I need to call John, finish the report, and buy groceries'"
   - "The AI extracts each task and adds them all at once"
   - "Command Mode: Give specific instructions like 'mark the report as done'"
   - "Making sense?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: How Tasks are Stored
   - "All tasks saved locally in tasks.json - no cloud, full privacy"
   - "Each task has: text, priority (high/medium/low), category (client/business/personal)"
   - "Tasks persist between sessions automatically"
   - "Questions about the data model?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]

3. After architecture basics: "Want to see what commands you can use?"
4. **CONTINUE TO NEXT SECTION or user's choice**

#### Path 2: Learn the Features
1. Read `.reference/voice-commands-guide.md` FIRST
2. Present features progressively:
   
   **Concept**: Adding Tasks
   - "You can add tasks in two ways:"
   - "Brain Dump: 'I need to review docs, call client, update timeline'"
   - "Direct: 'Add a high priority task to review the contract'"
   - "Want to know about other commands?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Task Management Commands
   - "Natural language works for everything:"
   - "• 'Mark the contract review as complete'"
   - "• 'Change the client call to high priority'"
   - "• 'Delete the grocery task'"
   - "• 'What should I work on next?'"
   - "Clear on how to manage tasks?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Smart Task Matching
   - "You don't need exact names - the system is smart"
   - "If your task is 'Review quarterly financial report'"
   - "You can say: 'complete the financial report' or 'mark quarterly review as done'"
   - "It uses fuzzy matching to find the right task"
   - "Makes sense?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: Queries and Filters
   - "Ask questions naturally:"
   - "• 'Show me all high priority tasks'"
   - "• 'What client tasks do I have?'"
   - "• 'How many tasks are pending?'"
   - "• 'Prioritize my tasks for me'"
   - "Questions about queries?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Concept**: AI Help Panel
   - "There's a built-in help assistant in the left sidebar"
   - "Click the help toggle and ask questions by voice or text"
   - "It knows the current state of your tasks and gives contextual help"
   - "Want to learn about the UI workflow?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]

3. After features: "Ready to try it yourself?"
4. **CONTINUE TO QUICK START or user's choice**

#### Path 3: Explore the Code
1. Read `.reference/task-tracker-architecture.md` Core Components section
2. Show the structure:
   
   ```bash
   ls -la services/  # Show all service files
   ```
   
   **Concept**: Service Organization
   - "Each service has a single responsibility:"
   - "Want to explore a specific service?"
   - "Options: whisper, llm, task_manager, command_router, tts, or help"
   [WAIT FOR USER RESPONSE - then read that service file]
   
   After showing service:
   - "This service [explain what it does based on the file]"
   - "Notice how it [point out key pattern]"
   - "Want to see another service or the main app?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
3. Based on interest, explore:
   - app.py for Streamlit UI
   - services/ for business logic
   - Show how they connect

#### Path 4: Just Get Started
1. Read `.reference/getting-started-guide.md` Quick Start section
2. Guide through setup:
   
   **Step 1**: Check Environment
   ```bash
   test -f .env && echo "✅ API key configured" || echo "⚠️ Need to set OPENAI_API_KEY in .env"
   test -d venv && echo "✅ Virtual environment exists" || echo "⚠️ Need to create venv"
   ```
   
   Based on results:
   - If missing .env: "Let's set up your OpenAI API key..."
   - If missing venv: "Let's create your virtual environment..."
   - If both exist: "Great! You're ready to go"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Step 2**: Install Dependencies (if needed)
   - "Let's install the requirements:"
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   - "Dependencies installed! Ready to launch?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Step 3**: Launch the App
   - "Starting the Voice Task Manager:"
   ```bash
   streamlit run app.py
   ```
   - "The app should open at http://localhost:8501"
   - "You'll see the recording button in the main area"
   - "Ready to try your first voice command?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Step 4**: First Voice Command
   - "Let's try Brain Dump mode (it's selected by default)"
   - "Click the microphone button"
   - "Try saying: 'I need to review the monthly report, schedule a team meeting, and update the project timeline'"
   - "The AI will extract your tasks and show them"
   - "Click 'Add to Task List' to save them"
   - "How did that work?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]
   
   **Step 5**: Try a Command
   - "Now switch to Command Mode (radio button at top)"
   - "Click record and say: 'Mark the monthly report as complete'"
   - "You'll hear voice feedback confirming the action"
   - "The task will show as completed with strikethrough"
   - "Want to learn more commands?"
   [WAIT FOR USER RESPONSE BEFORE CONTINUING]

### AFTER ANY PATH

Based on where they are, offer next steps:
- After Architecture → "Want to learn the commands?" → Path 2
- After Features → "Ready to try it?" → Path 4
- After Code → "Want to run it?" → Path 4
- After Quick Start → "Want to learn more features?" → Path 2

### HELP AT ANY TIME

**User can always say**:
- "I don't understand" → Explain current concept differently
- "Show me an example" → Provide concrete example
- "What can I say?" → Show voice command examples
- "I need help" → Offer assistance

### REMEMBER

- **ONE concept at a time** - Never dump multiple concepts
- **Always wait for response** - Don't continue without user input
- **Use .reference files** - They have accurate information
- **Guide the journey** - User should never wonder "what next?"
- **Be encouraging** - This is about learning, not testing