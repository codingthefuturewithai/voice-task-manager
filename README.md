# 🎤 Voice Task Manager

A powerful, AI-driven task management application that lets you manage your tasks through natural voice commands. Built with Streamlit and OpenAI's Whisper + GPT-5 nano.

## 🚀 Getting Started with AI Coding Assistants

### Learn This Voice Task Manager Interactively

This repository includes custom commands that help you explore and understand this specific application - its architecture, voice commands, UI workflows, and codebase - through interactive, step-by-step guidance with AI coding assistants.

#### How to Use:

**Claude Code:**
- Type `/getting-started` and press Enter

**Other AI Assistants (Cursor, etc.):**
- Drag `.claude/commands/getting-started.md` into the chat window and press Enter

#### Available Commands:

```bash
# Interactive guided tour - learn step by step
/getting-started

# Refresh the knowledge base from current code
/refresh-knowledge

# Discover UI elements and capabilities
/refresh-ui-elements
```

#### What These Commands Do:

- **`/getting-started`** - Interactive tutorial that teaches you:
  - The architecture and how components work together
  - All voice commands and capabilities
  - How to explore the code
  - Quick setup and your first voice command
  
- **`/refresh-knowledge`** - Analyzes the codebase and updates documentation:
  - Ensures all documentation matches current implementation
  - Updates architecture, commands, workflows, and setup guides
  - Run this after making significant changes

- **`/refresh-ui-elements`** - Discovers and documents UI capabilities:
  - Maps all interactive elements
  - Documents what each element actually does
  - Saves to `.reference/ui_elements.json`

### Traditional Setup

If you're not using an AI coding assistant, follow the manual installation steps in the [Quick Start](#-quick-start) section below.

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

### ❓ AI-Powered Help System
- **Dynamic assistance**: Ask questions about using the app
- **Voice and text input**: Get help through voice or typing
- **Context-aware suggestions**: Receive personalized tips based on your tasks
- **Quick reference**: Always-available command reference
- **Tutorial guidance**: Step-by-step help for new users

### 📈 Advanced Statistics
- Comprehensive task breakdown by priority and category
- Completion tracking and progress metrics
- Visual indicators for task status

## 📦 Quick Start

> **Note:** If you're using an AI coding assistant (Claude Code, Cursor, etc.), run `/getting-started` for an interactive setup guide instead.

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

### Getting Help
The Voice Task Manager includes an AI-powered help system:

1. **Access Help**: Click "🔧 Toggle Help Panel" in the sidebar
2. **Ask Questions**: Use voice or text to ask about features
3. **Get Suggestions**: View contextual tips based on your current tasks
4. **Quick Reference**: Access command reference anytime

**Example Help Questions:**
- "How do I add a task?"
- "What commands can I use?"
- "How do I change task priority?"
- "What should I work on next?"

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
- **GPT-5 nano**: 3x cheaper than GPT-4o-mini (which was ~$0.00015 per command)
- **Estimated daily cost** (heavy use): < $0.20

## 🏗️ Architecture

### Services
- **WhisperService**: Handles speech-to-text transcription
- **LLMService**: Processes commands and extracts tasks
- **TaskManager**: Manages task storage and operations
- **CommandRouter**: Routes voice commands to appropriate handlers
- **TTSService**: Provides voice feedback
- **TaskMatcher**: Fuzzy matching for natural language task references
- **HelpService**: AI-powered help system with knowledge base

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

## 📚 AI Assistant Integration

This repository includes a `.claude/` directory with custom commands specifically designed to help you understand and work with this Voice Task Manager application using AI coding assistants (Claude Code, Cursor, and others):

### Available Commands

**Using in Claude Code:**
- Type `/getting-started` (or any command) and press Enter

**Using in Other Assistants:**
- Drag the command file from `.claude/commands/` into the chat window and press Enter

**Commands:**
- **`getting-started.md`** - Interactive tutorial for learning the system
- **`refresh-knowledge.md`** - Update all documentation from current code
- **`refresh-ui-elements.md`** - Discover and document UI capabilities

### Knowledge Base

The `.reference/` directory contains comprehensive documentation:
- `task-tracker-architecture.md` - System architecture and components
- `voice-commands-guide.md` - All voice commands and patterns
- `user_workflows.md` - UI interactions and workflows
- `getting-started-guide.md` - Setup and usage instructions
- `ui_elements.json` - Discovered UI capabilities

These files are automatically maintained by the refresh commands to ensure documentation always matches the implementation.

---

**Built with ❤️ using Streamlit and OpenAI**