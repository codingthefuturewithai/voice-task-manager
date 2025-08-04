# 🎤 Voice Task Manager

A powerful, AI-driven task management application that lets you manage your tasks through natural voice commands. Built with Streamlit and OpenAI's Whisper + GPT-4o-mini.

## ✨ Features

### 🧠 Dual-Mode Operation
- **Brain Dump Mode**: Speak freely about multiple tasks and ideas - the AI will extract and organize them
- **Command Mode**: Give specific voice commands to manage existing tasks

### 🎯 Natural Language Commands
- **Add tasks**: "Add a task to review the documentation"
- **Modify tasks**: "Change the first task to high priority"
- **Delete tasks**: "Delete the task about testing"
- **Complete tasks**: "Mark the integration task as complete"
- **Query tasks**: "What should I work on next?"
- **Filter tasks**: "Show me all client tasks"
- **Prioritize**: "Prioritize my tasks for me"

### 📊 Enhanced Task Management
- **Priority levels**: High 🔴, Medium 🟡, Low 🟢
- **Categories**: Client 👤, Business 💼, Personal 🏠
- **Smart filtering**: Filter by priority, category, and status
- **Auto-prioritization**: AI suggests priorities based on task content
- **Task matching**: Natural language reference to existing tasks

### 🔊 Voice Feedback
- **Audio confirmations**: Hear back when actions are completed
- **Query responses**: Get spoken answers to your questions
- **Error handling**: Voice feedback for low-confidence commands

### 📈 Advanced Statistics
- Comprehensive task breakdown by priority and category
- Completion tracking and progress metrics
- Visual indicators for task status

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-tracker
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🎤 Usage Guide

### Brain Dump Mode (Default)
Perfect for capturing multiple tasks at once:

1. Select "🧠 Brain Dump" mode
2. Click the microphone and speak naturally
3. Example: *"I need to review the quarterly report, call the client about the project update, and schedule a team meeting for next week"*
4. The AI will extract and organize these into separate tasks
5. Click "Add to Task List" to save them

### Command Mode
Ideal for managing existing tasks:

1. Select "🎯 Command" mode
2. Give specific voice commands
3. Examples:
   - *"Add a high priority task to fix the login bug"*
   - *"Mark the documentation review as complete"*
   - *"What should I work on next?"*
   - *"Show me all client tasks"*
   - *"Delete the task about testing"*

### Voice Commands Reference

#### Adding Tasks
- "Add a task to [description]"
- "Create a [priority] priority task to [description]"
- "Add a [category] task to [description]"

#### Modifying Tasks
- "Change [task description] to [new description]"
- "Set [task description] to [priority] priority"
- "Mark [task description] as [category]"

#### Completing Tasks
- "Mark [task description] as complete"
- "Complete [task description]"
- "Finish [task description]"

#### Deleting Tasks
- "Delete [task description]"
- "Remove [task description]"
- "Cancel [task description]"

#### Queries
- "What should I work on next?"
- "Show me all [priority] priority tasks"
- "List all [category] tasks"
- "How many tasks do I have?"

#### Bulk Operations
- "Prioritize my tasks"
- "Clear all tasks"
- "Show me pending tasks"

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### API Costs
- **Whisper**: ~$0.006/minute of audio
- **GPT-4o-mini**: ~$0.00015 per command
- **Estimated daily cost** (heavy use): < $0.50

## 🏗️ Architecture

### Services
- **WhisperService**: Handles speech-to-text transcription
- **LLMService**: Processes commands and extracts tasks
- **TaskManager**: Manages task storage and operations
- **CommandRouter**: Routes voice commands to appropriate handlers
- **TTSService**: Provides voice feedback
- **TaskMatcher**: Fuzzy matching for natural language task references

### Data Model
```json
{
  "id": "uuid",
  "text": "Task description",
  "priority": "high|medium|low",
  "category": "client|business|personal|null",
  "completed": false,
  "created_at": "ISO timestamp",
  "modified_at": "ISO timestamp",
  "completed_at": "ISO timestamp|null"
}
```

## 🧪 Testing

### Voice Commands to Test
- [ ] "Add a task to review the documentation"
- [ ] "Change the first task to high priority"
- [ ] "Delete the task about testing"
- [ ] "Mark the integration task as complete"
- [ ] "What should I work on next?"
- [ ] "Show me all client tasks"
- [ ] "Prioritize my tasks for me"

### Edge Cases
- [ ] Empty task list
- [ ] Ambiguous task references
- [ ] Multiple tasks with similar names
- [ ] Network timeout during API calls
- [ ] Invalid audio input

## 🔮 Future Enhancements

- Multi-user support with authentication
- Cloud sync for cross-device access
- Recurring tasks and scheduling
- Calendar integration (Google, Outlook)
- Batch operations on multiple tasks
- Task dependencies and subtasks
- Time tracking per task
- Export to other formats (Markdown, CSV)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:
1. Check the console for error messages
2. Verify your OpenAI API key is valid
3. Ensure your microphone permissions are enabled
4. Try rephrasing your voice commands

---

**Built with ❤️ using Streamlit and OpenAI**