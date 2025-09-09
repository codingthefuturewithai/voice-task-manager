# Getting Started with Voice Task Manager

## Quick Start (For Experienced Users)

```bash
# 1. Ensure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Check dependencies
pip list | grep streamlit

# 3. Set OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 4. Run the application
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

## First-Time Setup

### Prerequisites
- Python 3.11 or higher
- Microphone access
- OpenAI API key
- Web browser

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

4. **Configure API Key**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Launch Application**
   ```bash
   streamlit run app.py
   ```

## Understanding the Interface

### Layout Overview
```
┌─────────────────────────────────────────────────────┐
│  🎤 Voice Task Manager                              │
├──────────────┬──────────────────────────────────────┤
│              │                                      │
│  Left Panel  │         Main Area                    │
│              │                                      │
│  - Mode      │    - Voice Recording Button          │
│    Selector  │    - Transcription Display           │
│              │    - Processed Tasks (Brain Dump)    │
│  - Help      │    - Command Results (Command Mode)  │
│    Panel     │                                      │
│              ├──────────────────────────────────────┤
│              │         Task List                    │
│              │                                      │
│              │    [✓] 🔴 💼 Task 1     [✏️] [🗑️]   │
│              │    [ ] 🟡 👤 Task 2     [✏️] [🗑️]   │
│              │    [ ] 🟢 🏠 Task 3     [✏️] [🗑️]   │
│              │                                      │
│              ├──────────────────────────────────────┤
│              │         Statistics                   │
│              │    Total: 3 | Pending: 2            │
└──────────────┴──────────────────────────────────────┘
```

### UI Elements

#### Mode Selector (Top Left)
- **🧠 Brain Dump**: Speak freely about multiple tasks
- **🎯 Command**: Give specific instructions

#### Recording Button (Main Area)
- **Click to start** recording
- **Automatic stop** after silence
- **Visual feedback** during recording

#### Task List (Right Side)
- **Checkbox**: Mark complete/incomplete
- **Priority**: 🔴 High, 🟡 Medium, 🟢 Low
- **Category**: 👤 Client, 💼 Business, 🏠 Personal
- **Edit Button** (✏️): Modify task text
- **Delete Button** (🗑️): Remove task

#### Help Panel (Left Sidebar)
- **Toggle button**: Show/hide help
- **Voice input**: Ask questions by voice
- **Text input**: Type questions
- **AI responses**: Context-aware help

## Your First Voice Command

### Step 1: Check Your Setup
1. Ensure microphone is connected
2. Browser has microphone permission
3. You see "Ready to record" status

### Step 2: Try Brain Dump Mode (Default)
1. Click "Click to record your voice"
2. Say: "I need to review the monthly report, schedule a team meeting for Friday, and update the project timeline"
3. Wait for processing
4. Review extracted tasks
5. Click "Add to Task List"

### Step 3: Try Command Mode
1. Switch to "🎯 Command" mode
2. Click record button
3. Say: "Mark the monthly report as complete"
4. Listen for voice confirmation
5. See task updated in list

## Common Workflows

### Morning Planning
1. Start in Brain Dump mode
2. Speak all tasks for the day
3. Review and add to list
4. Say "Prioritize my tasks"
5. Start with highest priority

### Quick Task Addition
1. Switch to Command mode
2. Say "Add a high priority task to call the client"
3. Task appears immediately

### Task Review
1. Say "What should I work on next?"
2. Listen to AI recommendation
3. Say "Show me all client tasks"
4. Review filtered list

### End of Day
1. Say "Show me completed tasks"
2. Review accomplishments
3. Say "What's left for tomorrow?"
4. Plan next day

## Voice Command Examples

### Essential Commands
- "Add a task to [do something]"
- "Mark [task name] as complete"
- "Delete [task name]"
- "What should I work on next?"
- "Show me all high priority tasks"

### Advanced Commands
- "Change [task] to high priority"
- "Categorize [task] as client"
- "Prioritize my tasks"
- "How many tasks are pending?"

## Troubleshooting

### Microphone Issues
- **No recording**: Check browser permissions
- **Can't hear playback**: Check system volume
- **Poor recognition**: Reduce background noise

### API Issues
- **No transcription**: Verify OpenAI API key
- **Slow response**: Check internet connection
- **Rate limits**: Wait a moment and retry

### Task Management
- **Can't find task**: Use more specific keywords
- **Wrong task selected**: Be more descriptive
- **Tasks not saving**: Check tasks.json permissions

## Tips for Success

### Speaking Tips
1. **Speak clearly** at normal pace
2. **Wait for beep** before speaking
3. **Pause briefly** between tasks in brain dump
4. **Use natural language**, not commands

### Organization Tips
1. **Use categories** to group related tasks
2. **Set priorities** for important items
3. **Review regularly** to stay on track
4. **Complete small tasks** first for momentum

### Efficiency Tips
1. **Brain dump** at start of day
2. **Command mode** for quick updates
3. **Voice queries** for status checks
4. **Keyboard shortcuts** when typing is faster

## Getting Help

### In-App Help
1. Click "🔧 Toggle Help Panel"
2. Ask questions like:
   - "How do I add a task?"
   - "What commands can I use?"
   - "How do I change priority?"

### Voice Help
1. In help panel, click microphone
2. Ask your question naturally
3. Get spoken and written response

### Documentation
- This guide: `.reference/getting-started-guide.md`
- Commands: `.reference/voice-commands-guide.md`
- Architecture: `.reference/task-tracker-architecture.md`

## Next Steps

### Customize Your Experience
1. Explore all voice commands
2. Set up your task categories
3. Develop your workflow

### Advanced Features
1. Try the AI-powered help system
2. Experiment with bulk operations
3. Use natural task references

### Extend the System
1. Review the architecture guide
2. Explore service implementations
3. Consider adding integrations