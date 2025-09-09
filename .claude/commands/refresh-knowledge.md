---
description: Analyze the codebase and update all .reference knowledge files to reflect the current implementation
argument-hint: "[--deep-analysis]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "MultiEdit", "Bash", "Task"]
---

## Refresh Knowledge Base

I need to analyze the Voice Task Manager codebase and update all knowledge files in `.reference/` to ensure they accurately reflect the current implementation.

This will update:
- `.reference/task-tracker-architecture.md` - System architecture and components
- `.reference/voice-commands-guide.md` - All voice commands and patterns
- `.reference/user_workflows.md` - UI interactions and workflows
- `.reference/getting-started-guide.md` - Setup and usage instructions

### Analysis Process

#### Phase 1: Codebase Discovery
Let the code reveal what this system actually is:
```bash
# Check project structure
ls -la
# Check for main entry point
ls *.py
# Check services directory
ls -la services/
# Check dependencies
cat requirements.txt
```

#### Phase 2: Architecture Analysis

##### 2.1 Technology Stack Discovery
- Read `requirements.txt` for actual dependencies
- Check imports in `app.py` and services files
- Identify the actual models/APIs used (search for "model", "gpt", "whisper")
- Find environment variables in code

##### 2.2 Service Architecture
For each file in `services/`:
- Read the file completely
- Document its actual purpose (from code, not filename)
- Trace its connections to other services
- Note the actual methods and their parameters

##### 2.3 Data Flow Mapping
Starting from `app.py`:
- Trace user input paths (button clicks, voice recording)
- Follow data through service calls
- Map state management (session_state keys)
- Document actual data structures used

##### 2.4 Update Architecture Documentation
Create/update `.reference/task-tracker-architecture.md` with:
- Actual technology stack (from requirements.txt and imports)
- Real service descriptions (from code analysis)
- True data flow (from tracing)
- Actual API costs/models (from service configurations)
- Real storage approach (from TaskManager)

#### Phase 3: Voice Commands Discovery

##### 3.1 Command Pattern Extraction
In `services/llm_service.py`:
- Find all prompts sent to the LLM
- Extract command examples from prompts
- Identify command categories from the code
- Document actual JSON structures expected

##### 3.2 Command Processing Logic
Trace through `services/command_router.py` (if exists) or LLMService:
- Find how commands are parsed
- Document confidence thresholds
- Identify error handling patterns
- Map command types to handlers

##### 3.3 Fuzzy Matching Analysis
In `services/task_matcher.py` (if exists) or relevant service:
- Understand matching algorithm
- Document similarity thresholds
- Extract matching examples

##### 3.4 Update Commands Documentation
Create/update `.reference/voice-commands-guide.md` with:
- All actual command patterns found in prompts
- Real examples from the code
- Actual matching logic
- True confidence handling

#### Phase 4: UI Workflows Tracing

##### 4.1 Interface Discovery
In `app.py`:
- Map all Streamlit components
- Find all user input methods (buttons, text inputs, audio)
- Document all display elements
- Trace session state usage

##### 4.2 Interaction Flows
For each user action:
- Start from UI element (button click, etc.)
- Follow the code path
- Document state changes
- Note feedback mechanisms (visual, audio)

##### 4.3 Mode Analysis
Find operating modes:
- Brain Dump vs Command mode logic
- State transitions
- UI differences between modes
- Processing differences

##### 4.4 Update Workflows Documentation
Create/update `.reference/user_workflows.md` with:
- Actual UI elements and their locations
- Real interaction sequences
- True state management
- Actual error handling

#### Phase 5: Setup & Configuration

##### 5.1 Requirements Analysis
- Parse `requirements.txt` for dependencies
- Check for `.env.example` or similar
- Find configuration requirements in code
- Identify optional vs required components

##### 5.2 Startup Process
- Trace `app.py` initialization
- Find service initialization order
- Document caching strategies (@st.cache_resource)
- Identify failure points

##### 5.3 API Configuration
- Find all API key usage
- Document rate limits if mentioned
- Identify costs from comments/docs
- Find fallback behaviors

##### 5.4 Update Getting Started Documentation
Create/update `.reference/getting-started-guide.md` with:
- Actual requirements from requirements.txt
- Real configuration needs
- True startup process
- Actual default ports/URLs

### Output Strategy

#### File Updates
For each `.reference/` file:
1. Read existing file (if exists) to understand structure
2. Preserve useful sections/formatting
3. Update with discovered information
4. Mark any outdated information
5. Ensure consistency across all files

#### Accuracy Principles
- Only document what IS in the code
- Never assume or infer beyond code evidence
- Include actual code snippets as proof
- Note where implementation differs from expectations
- Document actual model names, ports, URLs exactly as found

#### Validation
After updating all files:
- Cross-reference between files for consistency
- Ensure no contradictions
- Verify technical accuracy (model names, API calls)
- Check that examples match actual code

### Special Considerations

#### Model Names
- Search for "model" assignments
- Look for OpenAI API calls
- Document exactly what's used (e.g., "gpt-5-nano" not "gpt-4")

#### Costs and Limits
- Find any cost mentions in comments
- Look for rate limiting code
- Document actual values, not estimates

#### Browser vs Server Features
- Identify browser-native features (Web Speech API)
- Note server-side processing
- Document what runs where

### Execution Order

1. **Discover** - Understand the codebase structure
2. **Analyze** - Deep dive into each component
3. **Document** - Update knowledge files with findings
4. **Validate** - Ensure accuracy and consistency
5. **Report** - Summarize what was updated

---

## Important Notes

- Make no assumptions about functionality
- Let code patterns reveal the implementation
- Document actual behavior, not intended behavior
- Update means refresh from code, not minor edits
- All model names, costs, ports must match code exactly