# Voice Commands Guide for Task Tracker

## Overview
The Task Tracker supports natural language voice commands for managing tasks through two intelligent processing systems:
1. **LLMService**: Processes voice commands and detects user intent
2. **AgentService** (Optional): Provides advanced automation with 10 specialized task management tools

Simply speak naturally, and the AI will understand your intent and execute the appropriate actions.

## Supported Intents

The system recognizes 7 primary intents from voice commands:

### 1. Add Task (`add` intent)
Create a new task with optional priority and category.

**Basic Examples:**
- "Add a task to call the dentist"
- "Create a task to review the contract"
- "I need to send the invoice"
- "Remember to pick up groceries"

**With Priority:**
- "Add a high priority task to finish the report"
- "Create an urgent task to call the client"
- "Add a low priority task to organize desk"

**With Category:**
- "Add a client task to prepare presentation"
- "Create a business task to update budget"
- "Add a personal task to schedule dentist"

**Combined:**
- "Add a high priority client task to send proposal"
- "Create an urgent business task to fix the bug"

### 2. Complete Task (`complete` intent)
Mark a task as done/completed.

**Examples:**
- "Mark the dentist task as complete"
- "Complete the invoice task"
- "I finished the presentation"
- "Done with calling the client"
- "Check off the grocery shopping"
- "The report is finished"

### 3. Modify/Update Task (`modify` intent)
Change an existing task's text, priority, or category.

**Change Description:**
- "Change the meeting task to include agenda"
- "Update the presentation to add slides"
- "Rename the report task to quarterly report"

**Change Priority:**
- "Set the client call to high priority"
- "Make the bug fix urgent"
- "Change the meeting to low priority"
- "Increase priority on the proposal"

**Change Category:**
- "Move the dentist task to personal"
- "Set the presentation to client category"
- "Categorize the budget review as business"

### 4. Delete Task (`delete` intent)
Remove a task from the list.

**Examples:**
- "Delete the grocery shopping task"
- "Remove the old meeting task"
- "Cancel the dentist appointment"
- "Get rid of the completed presentation"
- "Drop the draft task"
- "Clear all completed tasks"

### 5. Query Tasks (`query` intent)
Ask questions about your tasks.

**Status Queries:**
- "What should I work on next?"
- "What's my highest priority?"
- "Show me pending tasks"
- "What have I completed today?"

**Filtered Queries:**
- "Show me all high priority tasks"
- "List all client tasks"
- "What business tasks do I have?"
- "Display urgent items"

**Count Queries:**
- "How many tasks do I have?"
- "How many are pending?"
- "What's my task count?"

### 6. Brain Dump Mode (`braindump` intent)
Quickly capture multiple tasks from stream-of-consciousness speech.

**Examples:**
- "I need to call the dentist tomorrow, finish the quarterly report by Friday, and remember to pick up dry cleaning"
- "Grocery shopping, pay bills, client presentation prep, workout schedule, book flights"
- Stream-of-consciousness speech with multiple action items

The system will:
- Extract individual actionable tasks
- Assign appropriate priorities based on urgency words
- Categorize tasks based on context
- Clean up filler words and make tasks concise

### 7. Prioritize Tasks (`prioritize` intent)
Get help organizing and prioritizing your task list.

**Examples:**
- "Help me prioritize my tasks"
- "What should I focus on first?"
- "Organize my tasks by importance"
- "Which tasks are most urgent?"
- "Suggest task priorities"
- "Auto-prioritize everything"

## Task Properties

### Priority Levels
- **High**: Urgent and important tasks
  - Keywords: urgent, ASAP, critical, important, immediately
- **Medium**: Default priority for most tasks
  - Default when no priority is specified
- **Low**: Tasks that can wait
  - Keywords: eventually, someday, when possible, low priority

### Categories
- **Client**: Client-related work and deliverables
  - Keywords: client, customer, presentation, proposal, meeting
- **Business**: Internal business tasks and operations
  - Keywords: business, internal, budget, report, planning
- **Personal**: Personal reminders and life tasks
  - Keywords: personal, home, family, doctor, grocery

## Task Reference Patterns

The system uses fuzzy matching to identify tasks:

### By Position
- "the first task"
- "the last task"
- "task number 3"
- "the second one"

### By Keywords
- "the documentation task"
- "the one about the meeting"
- "the budget review"
- "that client task"

### By Partial Matches
If task is "Review quarterly financial report":
- "the financial report"
- "quarterly review"
- "the report"

### By Properties
- "the high priority task"
- "that urgent one"
- "the client task"
- "my personal item"

## Agent Service Tools (When Available)

If the optional AgentService is initialized, these tools are available:

1. **list_tasks** - List tasks with filtering options
2. **add_task** - Create new tasks with priority and category
3. **complete_task** - Mark tasks as completed
4. **update_task** - Modify existing task properties
5. **delete_task** - Remove tasks from the system
6. **get_tasks_by_priority** - Filter tasks by priority level
7. **get_tasks_by_category** - Filter tasks by category
8. **get_pending_tasks** - Show only incomplete tasks
9. **get_completed_tasks** - Show only finished tasks
10. **get_task_stats** - Generate task statistics

## Voice Feedback Responses

### Success Confirmations
- "Task added successfully"
- "Task marked as complete"
- "Task deleted"
- "Priority updated to high"
- "Category changed to client"

### Query Responses
- "You have 5 pending tasks"
- "Your highest priority task is..."
- "Here are your client tasks..."
- "You should work on..."

### Error Handling
- "I couldn't find that task"
- "Please be more specific"
- "No tasks match your description"
- "Would you like me to create a new task instead?"

## Tips for Better Recognition

### Speaking Clearly
- Speak at normal pace
- Articulate clearly
- Minimize background noise
- Wait for the recording indicator

### Effective Commands
- Start with action verb (add, delete, mark, show)
- Be specific about what you want
- Use natural language, not keywords
- Include context when helpful

### Handling Ambiguity
- Use unique keywords from task text
- Mention priority or category if needed
- Use position for simple lists
- Be more specific if multiple matches exist

## Advanced Patterns

### Compound Commands
- "Add a task to call John and mark it as high priority"
- "Complete the report task and delete the draft"
- "Show me client tasks that are high priority"

### Bulk Operations
- "Mark all client tasks as high priority"
- "Complete all tasks containing 'email'"
- "Delete all completed tasks"
- "Clear everything and start fresh"

### Time References
- "Add task to call client tomorrow"
- "Remind me to submit report by Friday"
- "Schedule meeting for next week"
(Note: Time references are captured in task text, not scheduled)

## Confidence Scoring

The system provides confidence scores for command interpretation:

### High Confidence (>80%)
- Clear, unambiguous commands
- Exact task matches
- Well-formed sentences

### Medium Confidence (50-80%)
- Partial matches
- Slightly ambiguous references
- Minor grammar issues

### Low Confidence (<50%)
- Very ambiguous commands
- Multiple possible matches
- System asks for clarification

## Getting Help

### Voice Commands for Help
- "What can I say?"
- "Help me with commands"
- "Show me examples"
- "How do I add a task?"
- "What commands are available?"

### UI Help Button
Click the "Show Help" button in the interface for:
- Command reference
- Example patterns
- Tips and tricks
- Troubleshooting guide