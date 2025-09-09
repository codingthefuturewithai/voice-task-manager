# Voice Commands Guide

## Command Categories

### Task Addition Commands
Natural language patterns for adding tasks:

#### Basic Add
- "Add a task to [description]"
- "Create a task to [description]"
- "I need to [description]"
- "Remember to [description]"

#### With Priority
- "Add a high priority task to [description]"
- "Create an urgent task to [description]"
- "Add a low priority task to [description]"

#### With Category
- "Add a client task to [description]"
- "Create a business task to [description]"
- "Add a personal task to [description]"

#### Combined
- "Add a high priority client task to [description]"
- "Create an urgent business task to [description]"

### Task Modification Commands

#### Change Description
- "Change [task reference] to [new description]"
- "Update [task reference] to say [new description]"
- "Rename [task reference] to [new description]"

#### Change Priority
- "Set [task reference] to high priority"
- "Make [task reference] urgent"
- "Change [task reference] to low priority"
- "Deprioritize [task reference]"

#### Change Category
- "Mark [task reference] as client"
- "Set [task reference] to business"
- "Change [task reference] to personal"
- "Categorize [task reference] as [category]"

### Task Completion Commands
- "Mark [task reference] as complete"
- "Complete [task reference]"
- "Finish [task reference]"
- "Done with [task reference]"
- "Check off [task reference]"
- "I finished [task reference]"

### Task Deletion Commands
- "Delete [task reference]"
- "Remove [task reference]"
- "Cancel [task reference]"
- "Get rid of [task reference]"
- "Drop [task reference]"

### Query Commands

#### Status Queries
- "What should I work on next?"
- "What's my highest priority?"
- "Show me pending tasks"
- "What tasks are not done?"
- "What have I completed?"

#### Filtered Queries
- "Show me all high priority tasks"
- "List all client tasks"
- "What business tasks do I have?"
- "Show me personal tasks"
- "Display urgent items"

#### Count Queries
- "How many tasks do I have?"
- "How many are pending?"
- "How many are complete?"
- "What's my task count?"

### Bulk Operations

#### Prioritization
- "Prioritize my tasks"
- "Sort my tasks by priority"
- "Auto-prioritize everything"
- "Suggest priorities"

#### Clearing
- "Clear all tasks"
- "Delete everything"
- "Start fresh"
- "Remove all completed tasks"

#### Filtering
- "Hide completed tasks"
- "Show only pending"
- "Focus on high priority"

## Task Reference Patterns

The system uses fuzzy matching to identify tasks. You can reference tasks by:

### Position
- "the first task"
- "the last task"
- "the second one"
- "task number 3"

### Keywords
- "the documentation task"
- "the one about the meeting"
- "the budget review"
- "that client task"

### Partial Matches
- If task is "Review quarterly financial report"
  - "the financial report"
  - "quarterly review"
  - "the report"

### Priority/Category
- "the high priority task"
- "that urgent one"
- "the client task"
- "my personal item"

## Brain Dump Mode Patterns

In Brain Dump mode, speak naturally about multiple tasks:

### Sequential Lists
"I need to finish the report, call the client, and schedule a team meeting"
→ Creates 3 tasks

### Contextual Grouping
"For the project, I should review the specs, update the timeline, and send status updates"
→ Creates 3 business tasks

### Mixed Priorities
"Urgently fix the login bug, when I have time organize my desk, and don't forget the client call tomorrow"
→ Creates tasks with different priorities

### Time References
"Today I need to finish the presentation, tomorrow call the vendor, and by Friday submit the proposal"
→ Creates tasks (time references noted in description)

## Command Confidence

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
- Unclear intent
- System asks for clarification

## Voice Feedback Responses

The system provides voice confirmations:

### Success Responses
- "Task added successfully"
- "Task marked as complete"
- "Task deleted"
- "Priority updated to high"

### Query Responses
- "You have 5 pending tasks. The highest priority is..."
- "Here are your client tasks..."
- "You should work on..."

### Error Responses
- "I couldn't find that task"
- "Please be more specific"
- "No tasks match your description"

## Tips for Better Recognition

### Speaking Clearly
- Speak at normal pace
- Articulate clearly
- Avoid background noise
- Wait for the beep before speaking

### Command Structure
- Start with action verb (add, delete, mark, show)
- Be specific about what you want
- Use natural language, not keywords
- Include context when helpful

### Task References
- Use unique keywords from task text
- Mention priority or category if ambiguous
- Use position (first, last) for simple lists
- Be more specific if multiple matches exist

## Advanced Patterns

### Conditional Commands
- "If there are any high priority tasks, show them"
- "Mark all client tasks as high priority"
- "Complete all tasks containing 'email'"

### Compound Commands
- "Add a task to call John and mark it as high priority"
- "Complete the report task and delete the draft task"
- "Show me client tasks that are high priority"

### Meta Commands
- "What can I say?"
- "Help me with commands"
- "Show me examples"
- "How do I..."