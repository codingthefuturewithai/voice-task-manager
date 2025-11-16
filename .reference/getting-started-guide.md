# Getting Started with Voice Task Manager

## Quick Start (For Experienced Users)

```bash
# 1. Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Check dependencies
pip list | grep -E "streamlit|openai|langgraph"

# 3. Set OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 4. Run the application
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

## First-Time Setup

### Prerequisites
- Python 3.11 or higher
- Microphone access for voice input
- OpenAI API key (for Whisper and GPT-5 nano)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 500MB disk space for dependencies

### Installation Steps

1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd task-tracker
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Key dependencies installed:
   - `streamlit>=1.47.0` - Web UI framework
   - `openai>=1.12.0` - Whisper & GPT-5 nano API
   - `langgraph>=0.6.6` - Agent framework (optional enhancement)
   - `langchain-openai>=0.2.0` - LangChain integration
   - `python-dotenv>=1.0.0` - Environment management

4. **Configure API Key**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
   ```

   Get your API key from: https://platform.openai.com/api-keys

5. **Launch Application**
   ```bash
   streamlit run app.py
   ```

   The app will open at http://localhost:8501

## First Use Tutorial

### 1. Initial Interface
When you first open the app, you'll see:
- **Mode selector** (Brain Dump vs Command Mode)
- **Task list** (initially empty)
- **Voice recorder** button
- **Help button** for guidance

### 2. Adding Your First Tasks

#### Option A: Brain Dump Mode (Recommended for beginners)
1. Select "Brain Dump Mode" from the dropdown
2. Click the microphone button
3. Speak naturally about your tasks:
   > "I need to finish the quarterly report by Friday, call the dentist to schedule an appointment, and remember to pick up groceries on the way home"
4. Click stop recording
5. Watch as the AI extracts and organizes your tasks

#### Option B: Command Mode
1. Select "Command Mode"
2. Click the microphone button
3. Give a specific command:
   > "Add a high priority task to review the contract"
4. The task is added immediately

### 3. Managing Tasks

#### Voice Commands
- **Complete**: "Mark the dentist task as complete"
- **Update**: "Change the report task to high priority"
- **Delete**: "Remove the grocery task"
- **Query**: "Show me all high priority tasks"

#### UI Controls
Each task card has:
- ✅ **Checkbox** - Click to complete/uncomplete
- ✏️ **Edit button** - Modify task text, priority, category
- 🗑️ **Delete button** - Remove the task
- 🔊 **Listen button** - Hear task details

### 4. Task Organization

#### Priorities
Tasks are color-coded:
- 🔴 **High Priority** - Red background
- 🟡 **Medium Priority** - Yellow background
- 🟢 **Low Priority** - Green background

#### Categories
- **Client** - Client-related work
- **Business** - Internal business tasks
- **Personal** - Personal reminders

#### Statistics
The sidebar shows:
- Total tasks
- Completed count
- Breakdown by priority
- Breakdown by category

## Operating Modes Explained

### Brain Dump Mode
Best for:
- Morning planning sessions
- End-of-meeting action items
- Stream-of-consciousness capture
- Processing multiple tasks at once

How it works:
1. Speak freely about all your tasks
2. AI extracts individual action items
3. Assigns priorities based on urgency words
4. Categorizes based on context
5. Presents organized task list for review

### Command Mode
Best for:
- Quick single task additions
- Specific task updates
- Targeted queries
- Precise control

How it works:
1. Give a specific command
2. AI detects intent (add, complete, delete, etc.)
3. Executes action immediately
4. Provides voice confirmation

## Advanced Features

### Agent Service (Optional)
If initialized, provides:
- Automated task organization
- Bulk operations
- Advanced filtering
- Task statistics
- Multi-step automation

Check if available:
- Look for "✅ Agent service initialized" in console
- Or check Help panel for agent status

### Voice Feedback
The app uses browser speech synthesis to:
- Confirm task additions
- Read task summaries
- Provide status updates
- Answer queries verbally

### Task Persistence
- Tasks saved to `tasks.json`
- Automatic save on every change
- Survives app restarts
- Can be backed up or shared

## Troubleshooting

### Common Issues

#### "Microphone not working"
1. Check browser permissions (Settings → Privacy → Microphone)
2. Ensure microphone is not in use by another app
3. Try refreshing the page
4. Test microphone at: https://www.onlinemictest.com/

#### "OpenAI API key error"
1. Verify `.env` file exists and contains:
   ```
   OPENAI_API_KEY=sk-your-actual-key
   ```
2. Check key validity at: https://platform.openai.com/api-keys
3. Ensure key has Whisper and GPT-5 nano access
4. Restart the app after updating `.env`

#### "Tasks not saving"
1. Check `tasks.json` file permissions
2. Ensure disk has available space
3. Look for error messages in terminal
4. Try creating `tasks.json` manually:
   ```bash
   echo "[]" > tasks.json
   ```

#### "Agent service not available"
This is optional - the app works fine without it.
If you want to enable it:
1. Ensure `langgraph` is installed
2. Check for import errors in console
3. Verify all agent dependencies are met

### Performance Tips

1. **Voice Recognition**
   - Speak clearly and at normal pace
   - Minimize background noise
   - Wait for recording indicator
   - Keep commands under 30 seconds

2. **Task Management**
   - Use descriptive task names
   - Leverage categories for organization
   - Set appropriate priorities
   - Regular cleanup of completed tasks

3. **System Resources**
   - Close unnecessary browser tabs
   - Restart app if it becomes sluggish
   - Monitor `tasks.json` file size
   - Clear browser cache if needed

## Keyboard Shortcuts

While the app is primarily voice-driven, these shortcuts are available:
- **Space** - Start/stop recording (when focused)
- **Escape** - Cancel current operation
- **Tab** - Navigate between UI elements
- **Enter** - Confirm edits or actions

## API Usage & Costs

### OpenAI API Pricing (Approximate)
- **Whisper**: ~$0.006 per minute of audio
- **GPT-5 nano**: 3x cheaper than GPT-4o-mini
- Average monthly cost for daily use: <$5

### Usage Optimization
- Use Brain Dump mode for multiple tasks (single API call)
- Keep voice commands concise
- Leverage the Help system instead of trial-and-error
- Use UI controls when voice isn't needed

## Getting Help

### In-App Help
- Click "Show Help" button
- Say "What can I say?" for voice command help
- Check the status messages for guidance

### Documentation
- `.reference/voice-commands-guide.md` - Complete command reference
- `.reference/task-tracker-architecture.md` - Technical details
- `.reference/user_workflows.md` - Usage patterns

### Support
- GitHub Issues for bug reports
- Documentation in `.reference/` folder
- Code comments for implementation details

## Next Steps

1. **Master Voice Commands**
   - Practice with different phrasings
   - Learn the 7 intent types
   - Experiment with compound commands

2. **Optimize Your Workflow**
   - Find your preferred mode
   - Set up categories for your work
   - Develop command patterns

3. **Extend the System**
   - Customize categories in code
   - Add new voice commands
   - Integrate with other tools
   - Enable agent service for automation

## Quick Command Reference

### Essential Commands
- "Add a task to [description]"
- "Mark [task] as complete"
- "Show me my tasks"
- "Delete [task]"
- "What should I work on?"

### Priority Commands
- "Add a high priority task..."
- "Make [task] urgent"
- "Show me high priority tasks"

### Category Commands
- "Add a client task..."
- "Show me business tasks"
- "Move [task] to personal"

### Bulk Operations
- "Help me prioritize"
- "Clear completed tasks"
- "Show task statistics"

Happy task managing! 🎯