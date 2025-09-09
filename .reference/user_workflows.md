# Voice Task Manager - User Workflows

## Getting Started

### First Time User
1. **Open the application** at http://localhost:8501
2. **See the Help panel** in the left sidebar (collapsible)
3. **Notice Mode Selection** at the top of main area (Brain Dump is default)
4. **View empty task list** on the right with message "No tasks yet. Start speaking to add some!"

## Core Workflows

### Adding Multiple Tasks (Brain Dump Mode)
**Current Mode:** 🧠 Brain Dump (default)
**Location:** Left column under Mode Selection

1. User sees info box: "Brain Dump Mode: Speak freely about multiple tasks and ideas"
2. User clicks "Click to record your voice" button
3. User speaks naturally: "I need to finish the quarterly report, schedule a meeting with the team, and review the budget proposal"
4. Recording stops, audio player appears
5. System shows "Transcribing..." spinner
6. Raw transcription appears in text area
7. System shows "Processing brain dump..." spinner
8. AI Processed Tasks list appears with:
   - 🟡 💼 Finish the quarterly report
   - 🟡 💼 Schedule a meeting with the team
   - 🟡 💼 Review the budget proposal
9. User clicks "Add to Task List" button
10. Tasks appear in right column with checkboxes, priority indicators, and delete buttons

### Executing Commands (Command Mode)
**Mode Switch:** Click "🎯 Command" radio button
**Location:** Mode selector at top of main area

1. User switches to Command Mode
2. Info box changes to: "Command Mode: Give specific commands..."
3. User clicks "Click to record your voice"
4. User says: "Mark the quarterly report task as complete"
5. System processes command
6. Success message appears: "Task 'Finish the quarterly report' marked as complete"
7. Confidence metric shows: "Confidence: 92%"
8. Task in list shows strikethrough text
9. Statistics update automatically

### Editing a Task
**Location:** Task item in right column

1. User locates task in list
2. User clicks ✏️ button next to task text
3. Text changes to input field with current text
4. User types new text
5. User clicks 💾 Save button
6. Task updates immediately
7. Or user clicks ❌ Cancel to revert

### Using AI Help Assistant
**Location:** Left sidebar - Help & Assistance panel

1. User clicks sidebar to expand Help panel
2. Status shows "💡 Ready for questions"
3. User has two options:
   
   **Voice Option:**
   - Click "🎤 Ask with voice"
   - Ask: "How do I change a task's priority?"
   - See transcription of question
   
   **Text Option:**
   - Type in "💬 Or type your question" field
   - Enter: "How do I change a task's priority?"

4. Status changes to "🤔 Processing..."
5. Answer appears with specific instructions
6. User can:
   - Click "Clear Answer" to ask new question
   - Click "Reset All" to clear everything
   - Expand "📋 Quick Reference" for command list
   - Expand "💡 Suggestions" for contextual tips

### Task Priority Management
**Visual Indicators:**
- 🔴 High Priority
- 🟡 Medium Priority  
- 🟢 Low Priority

**Setting Priority:**
1. In Brain Dump mode: AI auto-detects from keywords
2. In Command mode: "Set the budget task to high priority"
3. Manual: Click priority emoji to cycle through options (if implemented)

### Task Categories
**Visual Indicators:**
- 👤 Client tasks
- 💼 Business tasks
- 🏠 Personal tasks

**Setting Category:**
1. AI detects from context: "Call client" → 👤
2. Command: "Move the report to business category"
3. Tasks without category show empty space

### Viewing Task Statistics
**Location:** Bottom of task list (right column)

Always visible:
- **Total Tasks:** Shows count of all tasks
- **Completed:** Count of checked tasks (left)
- **Pending:** Count of unchecked tasks (right)

### Deleting Tasks
**Methods:**

1. **Individual Delete:**
   - Click 🗑️ button on specific task
   - Task removed immediately (no confirmation)

2. **Voice Command (Command Mode):**
   - "Delete the budget task"
   - System confirms: "Delete 'Review the budget proposal'?"
   - User sees [✅ Confirm] [❌ Cancel] buttons

3. **Clear All:**
   - Click "Clear All Tasks" button at bottom of left column
   - Confirmation required
   - All tasks removed

## Contextual Behaviors

### When Task List is Empty
- Right column shows: "No tasks yet. Start speaking to add some!"
- Help suggestions mention: "Try saying 'Add a task to review documentation'"

### When High Priority Tasks Exist
- Help suggestions prioritize them: "You have 2 high-priority tasks"
- Suggests: "Try saying 'Show me all high priority tasks'"

### When All Tasks Complete
- Help suggestions: "All your tasks are complete! Great job!"
- Prompts: "Try adding new tasks with Brain Dump mode"

### Mode Switching
- Switching modes clears current audio processing
- Processed tasks not yet added are lost
- Transcription clears
- Command results clear

## Error Handling

### Low Confidence Commands
- Warning message appears
- Confidence shows < 70%
- System offers alternatives:
  - "Did you want to: [Add a new task] [Modify a task]"

### Failed Transcription
- Error message: "Could not transcribe audio"
- User prompted to try again

### Network Errors
- Error accessing OpenAI API
- Fallback to manual task entry

## Accessibility Features

### Keyboard Navigation
- Tab through all interactive elements
- Enter to activate buttons
- Space to toggle checkboxes

### Screen Reader Support
- Hidden labels for visual-only elements
- Aria labels for icon buttons
- Status announcements for mode changes

### Visual Feedback
- Color-coded priorities
- Emoji indicators for categories
- Strikethrough for completed tasks
- Spinners during processing