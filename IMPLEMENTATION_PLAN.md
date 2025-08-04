# Voice Task Manager - Enhancement Implementation Plan

## Executive Summary

The Voice Task Manager is a Streamlit-based web application that enables users to manage tasks through voice commands. Currently, it supports basic voice-to-text transcription and task creation. This document outlines a comprehensive enhancement plan to transform it into a more intelligent, conversational task management system.

## Current State

### What the App Does Now
1. **Voice Recording**: Uses Streamlit's native `st.audio_input` widget to capture audio
2. **Speech-to-Text**: Processes audio through OpenAI's Whisper API ($0.006/minute)
3. **Task Extraction**: Uses GPT-4o-mini to clean and organize brain dumps into tasks
4. **Task Storage**: Persists tasks locally in JSON format
5. **Basic Operations**: Check off tasks as complete, delete individual tasks, clear all tasks

### Tech Stack
- **Frontend**: Streamlit (v1.47.0+)
- **Speech Recognition**: OpenAI Whisper API
- **LLM**: OpenAI GPT-4o-mini ($0.00015/1M input tokens)
- **Storage**: Local JSON file
- **Language**: Python 3.11+

### Current Limitations
- Only supports adding new tasks from voice input
- Cannot modify existing tasks
- No task prioritization or categorization
- All transcribed content is treated as new tasks
- No voice feedback
- Limited command understanding

## Intended Improvements

### Core Enhancements
1. **Dual-Mode Operation**
   - Brain Dump Mode (default): Current behavior for free-form task entry
   - Command Mode: Single-intent operations on existing tasks

2. **Natural Language Commands**
   - Add, modify, delete tasks using conversational language
   - Query tasks ("What should I work on next?")
   - Bulk operations ("Prioritize my tasks")

3. **Task Enrichment**
   - Priority levels (high, medium, low)
   - Categories/Tags (client, business, personal)
   - Modification timestamps

4. **Voice Feedback**
   - Audio confirmation of actions
   - Status updates spoken back to user

5. **Smart Task Matching**
   - Natural language reference to tasks
   - Fuzzy matching for task identification

## Detailed Implementation Guide

### Phase 1: Data Model Enhancement

#### 1.1 Update Task Structure
**File**: `services/task_manager.py`

```python
# Current structure
{
    'id': str,
    'text': str,
    'completed': bool,
    'created_at': str,
    'completed_at': str or None
}

# Enhanced structure
{
    'id': str,
    'text': str,
    'priority': 'high' | 'medium' | 'low',  # NEW
    'category': 'client' | 'business' | 'personal' | None,  # NEW
    'completed': bool,
    'created_at': str,
    'modified_at': str,  # NEW
    'completed_at': str or None
}
```

**Implementation Steps**:
1. Update `TaskManager.add_task()` to accept priority and category parameters
2. Add `TaskManager.update_task()` method for modifications
3. Create migration function for existing tasks.json files
4. Add `TaskManager.get_tasks_by_priority()` and `get_tasks_by_category()` methods

### Phase 2: Command Processing System

#### 2.1 Create Command Router Service
**New File**: `services/command_router.py`

```python
class CommandRouter:
    def __init__(self, llm_service, task_manager):
        self.llm = llm_service
        self.tasks = task_manager
    
    def process_command(self, transcription: str, mode: str, current_tasks: list) -> dict:
        """
        Route transcribed text to appropriate handler based on mode and intent
        Returns: {
            'intent': 'add|modify|delete|query|prioritize|braindump',
            'confidence': float,
            'target_task': dict or None,
            'new_content': str or None,
            'priority': str or None,
            'category': str or None,
            'tasks': list  # for braindump mode
        }
        """
```

#### 2.2 Enhance LLM Service
**File**: `services/llm_service.py`

Add new methods:
- `detect_intent()`: Classify user intent from transcription
- `match_task()`: Find task by natural language description
- `prioritize_tasks()`: Suggest task priorities based on content
- `suggest_next_task()`: Recommend what to work on

**LLM Prompt Template for Intent Detection**:
```python
INTENT_PROMPT = """
You are a task management assistant. Analyze the following voice command and determine the user's intent.

Current tasks:
{tasks_json}

User said: "{transcription}"

Classify the intent as one of:
- add: User wants to create a new task
- modify: User wants to change an existing task
- delete: User wants to remove a task
- complete: User wants to mark a task as done
- query: User is asking a question about tasks
- prioritize: User wants help organizing task priorities

Also identify:
- Which task they're referring to (if applicable)
- New content (for add/modify)
- Priority level mentioned (high/medium/low)
- Category mentioned (client/business/personal)

Return JSON only:
{
    "intent": "...",
    "confidence": 0.0-1.0,
    "target_task_id": "..." or null,
    "new_content": "..." or null,
    "priority": "..." or null,
    "category": "..." or null
}
"""
```

### Phase 3: Voice Feedback System

#### 3.1 Text-to-Speech Options

**Option A: Browser-Native (Recommended for simplicity)**
```javascript
// Add to Streamlit via components
const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.2;
    window.speechSynthesis.speak(utterance);
}
```

**Option B: OpenAI TTS API**
- Cost: $0.015/1K characters (tts-1) or $0.030/1K characters (tts-1-hd)
- Higher quality but adds latency and cost

**Implementation**: Create `services/tts_service.py`
```python
class TTSService:
    def __init__(self, method='browser'):  # or 'openai'
        self.method = method
        
    def speak(self, text: str):
        if self.method == 'browser':
            # Use Streamlit component to trigger browser TTS
            st.components.v1.html(f'''
                <script>
                const utterance = new SpeechSynthesisUtterance("{text}");
                window.speechSynthesis.speak(utterance);
                </script>
            ''', height=0)
        else:
            # Use OpenAI TTS API
            pass
```

### Phase 4: UI Enhancement

#### 4.1 Mode Selector
**File**: `app.py`

```python
# Add mode selector at top
mode = st.radio(
    "Mode",
    ["🧠 Brain Dump", "🎯 Command"],
    horizontal=True,
    index=0  # Default to Brain Dump
)

# Store in session state
if 'mode' not in st.session_state:
    st.session_state.mode = 'braindump'
```

#### 4.2 Enhanced Task Display
```python
# Add priority badges and category tags
def render_task(task):
    priority_colors = {
        'high': '🔴',
        'medium': '🟡', 
        'low': '🟢'
    }
    category_labels = {
        'client': '👤',
        'business': '💼',
        'personal': '🏠'
    }
    
    # Display with visual indicators
    col1, col2, col3, col4, col5 = st.columns([1, 1, 6, 1, 1])
    # ... render task with priority and category
```

#### 4.3 Confirmation Dialogs
```python
# For destructive operations
if intent == 'delete':
    st.warning(f"Delete '{target_task['text']}'?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm"):
            task_manager.delete_task(target_task['id'])
            tts_service.speak("Task deleted")
    with col2:
        if st.button("❌ Cancel"):
            st.rerun()
```

### Phase 5: Natural Language Task Matching

#### 5.1 Fuzzy Matching Implementation
**File**: `services/task_matcher.py`

```python
from difflib import SequenceMatcher

class TaskMatcher:
    @staticmethod
    def find_best_match(query: str, tasks: list) -> dict:
        """
        Find task that best matches natural language description
        Uses fuzzy string matching and keyword extraction
        """
        best_match = None
        best_score = 0
        
        for task in tasks:
            score = SequenceMatcher(None, query.lower(), task['text'].lower()).ratio()
            if score > best_score and score > 0.6:  # 60% similarity threshold
                best_score = score
                best_match = task
                
        return best_match
```

### Phase 6: Testing & Error Handling

#### 6.1 Add Comprehensive Error Handling
- Network failures (OpenAI API)
- Invalid audio input
- Ambiguous commands
- No matching tasks found

#### 6.2 Add Fallback Options
```python
# When intent detection fails
if confidence < 0.7:
    st.info("I'm not sure what you meant. Did you want to:")
    if st.button("➕ Add a new task"):
        # Process as add
    if st.button("📝 Modify a task"):
        # Show task list for selection
    # etc.
```

## Dependencies to Add

```txt
# Add to requirements.txt
streamlit-components-v1>=0.1.0  # For custom JavaScript
```

## Migration Guide

### For Existing Users
1. Backup current `tasks.json`
2. Run migration script (create `migrate_tasks.py`)
3. Test with existing data

### Migration Script
```python
def migrate_tasks():
    """Convert old task format to new format"""
    old_tasks = load_old_tasks()
    new_tasks = []
    for task in old_tasks:
        task['priority'] = 'medium'  # Default
        task['category'] = None
        task['modified_at'] = task['created_at']
        new_tasks.append(task)
    save_new_tasks(new_tasks)
```

## Testing Checklist

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

## Performance Considerations

### API Costs
- Whisper: ~$0.006/minute of audio
- GPT-4o-mini: ~$0.00015 per command (minimal)
- TTS (if using OpenAI): ~$0.015/1K characters
- **Estimated cost per day (heavy use)**: < $0.50

### Latency Optimization
1. Cache common responses
2. Preload TTS for common confirmations
3. Use session state to avoid re-processing
4. Implement request debouncing

## Future Enhancements (Not in Current Scope)

1. **Multi-user support** with authentication
2. **Cloud sync** for cross-device access
3. **Recurring tasks** and scheduling
4. **Integration with calendars** (Google, Outlook)
5. **Batch operations** on multiple tasks
6. **Task dependencies** and subtasks
7. **Time tracking** per task
8. **Export to other formats** (Markdown, CSV)

## Implementation Order

1. **Phase 1**: Data model (2 hours)
2. **Phase 2**: Command routing (3 hours)
3. **Phase 3**: Voice feedback (1 hour)
4. **Phase 4**: UI updates (2 hours)
5. **Phase 5**: Natural language matching (1 hour)
6. **Phase 6**: Testing & polish (1 hour)

**Total estimated time**: 10 hours

## Success Criteria

The enhancement is complete when:
1. Users can add, modify, and delete tasks using natural language
2. Tasks have visible priorities and categories
3. Voice feedback confirms actions
4. Command mode correctly interprets 90%+ of common commands
5. The system gracefully handles ambiguous inputs
6. All existing functionality remains intact