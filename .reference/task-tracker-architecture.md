# Task Tracker Architecture Guide

## Overview
The Voice Task Manager is a Streamlit-based web application that enables natural voice interaction for task management. It uses OpenAI's Whisper for speech-to-text and GPT-5 nano for natural language understanding, with an optional advanced agent service powered by LangGraph for automated task operations.

## Technology Stack

### Core Technologies
- **Python 3.11+** - Primary language
- **Streamlit** - Web UI framework
- **OpenAI API** - Whisper (speech-to-text) and GPT-5 nano (NLU)
- **JSON** - Local task storage
- **dotenv** - Environment configuration

### Key Libraries
- `streamlit` - Web application framework
- `openai` - API client for Whisper and GPT
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation and settings management
- `langgraph` - Agent framework for advanced automation (optional enhancement)
- `langchain-openai` - LangChain OpenAI integration
- `langchain-core` - Core LangChain tools and utilities
- Browser-native APIs for speech synthesis (no external TTS libraries)

## Architecture Patterns

### Service-Oriented Architecture
The application follows a clean service-oriented architecture with separation of concerns:

```
app.py (Main UI Layer)
    ↓
Services Layer
    ├── WhisperService (Speech-to-Text)
    ├── LLMService (Natural Language Understanding)
    ├── TaskManager (Task CRUD operations)
    ├── TTSService (Text-to-Speech feedback)
    ├── HelpService (AI-powered help system)
    └── AgentService (Optional: Advanced task automation)
```

### Data Flow

#### Voice Input Flow
1. **Audio Capture** → Microphone records user speech
2. **Transcription** → WhisperService converts to text
3. **Understanding** → LLMService extracts intent and entities
4. **Execution** → TaskManager performs operations
5. **Feedback** → TTSService provides voice confirmation

#### Operating Modes
- **Brain Dump Mode**: Free-form speech → Multiple task extraction
- **Command Mode**: Specific commands → Direct execution

## Core Components

### Main Application (app.py)
- Streamlit UI configuration
- Service initialization and caching
- Session state management
- UI component rendering
- Event handling

### Service Layer (services/)

#### WhisperService (whisper_service.py)
- Audio transcription via OpenAI Whisper API
- Handles speech-to-text conversion
- Returns transcribed text with confidence

#### LLMService (llm_service.py)
- Natural language understanding
- Command parsing and intent extraction
- Task extraction from brain dumps
- Structured output generation

#### TaskManager (task_manager.py)
- Task CRUD operations
- JSON file persistence
- Task filtering and searching
- Statistics generation
- Fuzzy matching for natural references

#### TTSService (tts_service.py)
- Browser-native speech synthesis (Web Speech API)
- No external TTS libraries required
- Voice confirmations for actions
- Fallback to visual messages if speech not supported

#### HelpService (help_service.py)
- AI-powered help system
- Knowledge base queries
- Context-aware suggestions
- Tutorial guidance

#### AgentService (agent_service.py) - Optional Enhancement
- LangGraph-based intelligent agent using create_react_agent
- Direct LangChain tool integration for task automation
- Autonomous task management with 10 specialized tools:
  - `list_tasks` - List tasks with filtering options
  - `add_task` - Create new tasks with priority and category
  - `complete_task` - Mark tasks as completed
  - `update_task` - Modify existing task properties
  - `delete_task` - Remove tasks from the system
  - `get_tasks_by_priority` - Filter tasks by priority level
  - `get_tasks_by_category` - Filter tasks by category
  - `get_pending_tasks` - Show only incomplete tasks
  - `get_completed_tasks` - Show only finished tasks
  - `get_task_stats` - Generate task statistics
- Graceful fallback if not available (app works without it)

## Data Model

### Task Structure
```json
{
  "id": "uuid4-string",
  "text": "Task description",
  "priority": "high|medium|low",
  "category": "client|business|personal|null",
  "completed": false,
  "created_at": "ISO-8601 timestamp",
  "modified_at": "ISO-8601 timestamp",
  "completed_at": "ISO-8601 timestamp or null"
}
```

### Storage
- Tasks stored in `tasks.json`
- Automatic file creation on first run
- Atomic writes to prevent corruption
- In-memory caching for performance

## Session State Management

### Streamlit Session State Keys
- `mode` - Current operating mode (brain_dump/command)
- `show_help` - Help panel visibility
- `edit_{task_id}` - Edit mode for specific tasks
- `audio_bytes` - Recorded audio data
- `transcription` - Latest transcription
- `processed_tasks` - Extracted tasks from brain dump
- `command_result` - Latest command execution result

## API Integration

### OpenAI API Usage
- **Whisper API**: Audio transcription (~$0.006/minute)
- **GPT-5 nano**: Natural language processing (3x cheaper than GPT-4o-mini, 3x more context)
- **Rate limiting**: Built-in retry logic
- **Error handling**: Graceful degradation

## Security Considerations

### API Key Management
- Stored in `.env` file (not in version control)
- Loaded via `python-dotenv`
- Validated at service initialization

### Data Privacy
- Tasks stored locally only
- No cloud sync by default
- Audio not retained after processing

## Performance Optimizations

### Caching Strategy
- `@st.cache_resource` for service initialization
- Services persist across reruns
- Lazy loading of optional components

### Efficient Updates
- Minimal UI redraws
- Selective component updates
- Session state for UI persistence

## Error Handling

### Graceful Degradation
- Optional services (AgentService) don't block startup
- API failures show user-friendly messages
- Fallback to manual input on voice failure

### User Feedback
- Clear error messages
- Voice feedback for confirmations
- Visual indicators for processing states

## Extension Points

### Adding New Services
1. Create service class in `services/`
2. Initialize in `init_services()`
3. Pass to components needing it

### Adding New Commands
1. Update LLMService prompt
2. Add command handler logic
3. Update help documentation

### Integration Opportunities
- Calendar systems (Google, Outlook)
- Project management tools (Jira, Asana)
- Note-taking apps (Notion, Obsidian)
- Time tracking systems