# Voice Task Manager - Complete Help Knowledge Base

## Application Overview
The Voice Task Manager is a voice-controlled task management application that uses AI to help you organize your tasks efficiently. It runs in your web browser at http://localhost:8502.

## User Interface Layout

### Main Layout Structure
- **Left Sidebar**: Collapsible Help & Assistance panel
- **Main Area**: Split into two columns
  - **Left Column (1/3 width)**: Voice Input controls
  - **Right Column (2/3 width)**: Task List display

### Help & Assistance Panel (Left Sidebar)
Located in the collapsible left sidebar with a ❓ icon. This is your AI assistant that can answer questions about the application.

**Components:**
- **Status Indicator**: Shows current state (✅ Response ready, 🤔 Processing, 💡 Ready)
- **Voice Input**: Click "🎤 Ask with voice" to ask questions verbally
- **Text Input**: Type questions in "💬 Or type your question" field
- **Answer Display**: Shows AI responses to your questions
- **Action Buttons**: 
  - "Clear Answer" - Clears current response
  - "Reset All" - Clears both question and answer
- **Quick Reference** (expandable): Common voice commands list
- **Suggestions** (expandable): Context-aware tips based on your current tasks

## Operating Modes

### 🧠 Brain Dump Mode (Default)
**Purpose**: Extract multiple tasks from natural, free-form speech
**Location**: Selected via radio button at top of main area
**How to use**: 
1. Speak naturally about all your tasks
2. AI extracts and organizes them
3. Review and add all at once

**Example**: "I need to finish the report, call John about the project, and buy groceries on the way home"

### 🎯 Command Mode
**Purpose**: Execute specific actions on existing tasks
**Location**: Selected via radio button at top of main area
**How to use**:
1. Switch to Command Mode
2. Give specific commands
3. System executes immediately

**Example**: "Mark the report task as complete"

## Voice Commands Reference

### Adding Tasks
- **Brain Dump Mode**: Just speak naturally about what you need to do
- **Command Mode**: 
  - "Add a task to [description]"
  - "Create a task for [description]"
  - "I need to [description]"

### Completing Tasks
- "Mark [task] as complete"
- "Mark [task] as done"
- "Complete [task]"
- "Check off [task]"
- "Finish [task]"

### Modifying Tasks
- "Change [task] to [new description]"
- "Update [task] to say [new text]"
- "Rename [task] to [new name]"
- "Edit [task]"

### Setting Priority
- "Set [task] to high priority"
- "Make [task] high/medium/low priority"
- "Change priority to high/medium/low"

Priority Indicators:
- 🔴 = High Priority
- 🟡 = Medium Priority
- 🟢 = Low Priority

### Setting Category
- "Move [task] to client category"
- "Set [task] as business/personal"
- "Categorize [task] as client/business/personal"

Category Indicators:
- 👤 = Client
- 💼 = Business
- 🏠 = Personal

### Deleting Tasks
- "Delete [task]"
- "Remove [task]"
- "Get rid of [task]"
- "Clear [task]"

### Querying Tasks
- "Show me all tasks"
- "What are my high priority tasks?"
- "Show me client tasks"
- "How many tasks do I have?"
- "What should I work on next?"
- "Show me pending tasks"

### Bulk Operations
- "Clear all tasks" (button at bottom of left column)
- "Delete all completed tasks"
- "Show me everything"

## Referring to Tasks in Commands

You can refer to tasks in three ways:

1. **By Content**: "the report task", "the one about calling John"
2. **By Position**: "the first task", "the second one", "the last task"
3. **By Keywords**: "the task with grocery in it"

## Task Management Features

### Task Components
Each task displays:
1. **Checkbox** (leftmost): Click to mark complete/incomplete
2. **Priority Emoji**: Shows priority level
3. **Task Text**: The task description (click ✏️ to edit)
4. **Category Emoji**: Shows category if set
5. **Delete Button** (🗑️): Remove individual task

### Editing Tasks
1. Click the ✏️ button next to any task
2. Text becomes editable
3. Click 💾 to save or ❌ to cancel

### Task Statistics
Bottom of task list shows:
- **Total Tasks**: All tasks count
- **Completed**: Checked tasks count
- **Pending**: Unchecked tasks count

## Audio Recording

### How to Record
1. Click "Click to record your voice" button
2. Speak clearly
3. Click stop when done
4. Audio player appears for playback
5. Transcription shows in text area below

### Processing Steps
1. **Transcribing...**: Converting speech to text
2. **Raw Transcription**: Shows exactly what was heard
3. **Processing...**: AI analyzing the content
4. **Results**: 
   - Brain Dump: List of extracted tasks
   - Command: Success/failure message with confidence score

## Troubleshooting

### If voice recording doesn't work:
- Check browser permissions for microphone
- Ensure you're using a modern browser (Chrome, Firefox, Safari)
- Try refreshing the page

### If commands aren't understood:
- Check the Confidence score (should be >70%)
- Speak more clearly and specifically
- Use exact command phrases from this guide
- Switch to Command Mode for single actions

### If tasks aren't appearing:
- In Brain Dump mode: Click "Add to Task List" after processing
- In Command mode: Commands execute immediately
- Check for error messages

### If the AI assistant doesn't respond:
- Check your internet connection
- Verify OpenAI API key is set
- Try clicking "Reset All" and asking again

## Tips for Best Results

### For Brain Dumps:
- Speak naturally but clearly
- Mention all tasks in one recording
- Include priority words: "urgent", "important", "whenever"
- Include category hints: "client call", "personal errand"

### For Commands:
- Be specific about which task
- Use clear action words
- One command at a time
- Wait for confirmation

### For Task Organization:
- High priority = urgent, must do today
- Medium priority = should do soon
- Low priority = can wait

## Keyboard Shortcuts
- **Tab**: Navigate between elements
- **Enter**: Activate buttons
- **Space**: Toggle checkboxes
- **Escape**: Cancel editing

## Quick Start Guide

1. **First Task**: Click record → Say "I need to write a report" → Add to list
2. **Multiple Tasks**: Stay in Brain Dump → Speak all tasks → Add all
3. **Complete Task**: Switch to Command → Say "mark the report as done"
4. **Get Help**: Ask the AI assistant "How do I prioritize tasks?"

## Common Questions

**Q: How do I change a task's priority?**
A: Either say "Set [task] to high priority" in Command mode, or edit the task manually.

**Q: Can I add multiple tasks at once?**
A: Yes! Use Brain Dump mode (default) and speak naturally about all your tasks.

**Q: How do I know which mode I'm in?**
A: Look at the Mode Selection radio buttons at the top. The selected mode shows which is active.

**Q: What happens if I switch modes while recording?**
A: The recording will be processed in the new mode. Previous unprocessed content is cleared.

**Q: Can I undo deleting a task?**
A: No, deletions are permanent. Be careful with the delete button.

**Q: How accurate is the voice recognition?**
A: Very accurate using OpenAI's Whisper. Speak clearly for best results.

**Q: Can I use this offline?**
A: No, it requires internet for the OpenAI API.

## Data Storage
- Tasks are stored locally in tasks.json
- No data is sent to external servers except for AI processing
- Your tasks persist between sessions