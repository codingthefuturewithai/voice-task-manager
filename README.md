# Voice Task Manager

A simple Streamlit app for voice-controlled task management using OpenAI's Whisper and GPT-4o-mini.

## Features

- 🎤 Voice input for brain dumping
- 🤖 AI-powered task organization (GPT-4o-mini)
- 📝 Clean task list management
- ✅ Check off completed tasks
- 🗑️ Delete individual tasks
- 📊 Task statistics

## Setup

1. Create and activate a Python virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. Run the app:
```bash
# Default port (8501)
streamlit run app.py

# Custom port if 8501 is already in use
streamlit run app.py --server.port 8502
```

## Architecture

- **Whisper API**: Speech-to-text transcription ($0.006/minute)
- **GPT-4o-mini**: Process brain dumps into organized tasks ($0.00015/1M input tokens)
- **Streamlit**: Web UI framework
- **Local JSON**: Task persistence

## Usage

1. Click the microphone button to start recording
2. Speak your brain dump or tasks
3. AI will transcribe and organize your thoughts
4. Review and add the organized tasks to your list
5. Check off tasks as you complete them