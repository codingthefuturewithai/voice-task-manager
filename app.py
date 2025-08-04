import streamlit as st
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from pathlib import Path

from services.whisper_service import WhisperService
from services.llm_service import LLMService
from services.task_manager import TaskManager
from services.command_router import CommandRouter
from services.tts_service import TTSService
from services.task_matcher import TaskMatcher

load_dotenv()

st.set_page_config(
    page_title="Voice Task Manager",
    page_icon="🎤",
    layout="wide"
)

@st.cache_resource
def init_services():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set your OPENAI_API_KEY in the .env file")
        st.stop()
    
    whisper = WhisperService(api_key)
    llm = LLMService(api_key)
    task_manager = TaskManager()
    command_router = CommandRouter(llm, task_manager)
    tts_service = TTSService()
    task_matcher = TaskMatcher()
    
    return whisper, llm, task_manager, command_router, tts_service, task_matcher

def render_task(task, task_manager, tts_service):
    """Render a single task with enhanced UI and editing capabilities"""
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
    
    # Initialize session state for editing
    edit_key = f"edit_{task['id']}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False
    
    col_check, col_priority, col_task, col_category, col_delete = st.columns([1, 1, 6, 1, 1])
    
    with col_check:
        if st.checkbox("Done", value=task["completed"], key=f"check_{task['id']}", label_visibility="hidden"):
            print(f"DEBUG: Checkbox clicked for task {task['id']}")
            task_manager.toggle_task(task['id'])
            tts_service.speak_confirmation('task_completed')
            st.rerun()
    
    with col_priority:
        priority_emoji = priority_colors.get(task.get('priority', 'medium'), '⚪')
        st.write(priority_emoji)
    
    with col_task:
        if st.session_state[edit_key]:
            # Edit mode
            new_text = st.text_input("Edit task:", value=task['text'], key=f"text_{task['id']}")
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button("💾", key=f"save_{task['id']}"):
                    print(f"DEBUG: Save button clicked for task {task['id']}")
                    task_manager.update_task(task['id'], text=new_text)
                    st.session_state[edit_key] = False
                    tts_service.speak_confirmation('task_updated')
                    st.rerun()
            with col_cancel:
                if st.button("❌", key=f"cancel_{task['id']}"):
                    print(f"DEBUG: Cancel button clicked for task {task['id']}")
                    st.session_state[edit_key] = False
        else:
            # Display mode
            if task["completed"]:
                st.markdown(f"~~{task['text']}~~")
            else:
                st.markdown(task['text'])
            
            # Edit button
            if st.button("✏️", key=f"edit_btn_{task['id']}"):
                print(f"DEBUG: Edit button clicked for task {task['id']}")
                st.session_state[edit_key] = True
    
    with col_category:
        if task.get('category'):
            category_emoji = category_labels.get(task['category'], '📝')
            st.write(category_emoji)
        else:
            st.write("")
    
    with col_delete:
        if st.button("🗑️", key=f"del_{task['id']}"):
            print(f"DEBUG: Delete button clicked for task {task['id']} - {task['text']}")
            task_manager.delete_task(task['id'])
            tts_service.speak_confirmation('task_deleted')
            st.rerun()

def render_stats(stats):
    """Render enhanced statistics"""
    st.subheader("📊 Task Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Tasks", stats['total'])
        st.metric("Completed", stats['completed'])
        st.metric("Pending", stats['pending'])
    
    with col2:
        st.metric("High Priority", stats['high_priority'], delta=stats['high_priority'])
        st.metric("Medium Priority", stats['medium_priority'])
        st.metric("Low Priority", stats['low_priority'])
    
    with col3:
        st.metric("Client Tasks", stats['client_tasks'])
        st.metric("Business Tasks", stats['business_tasks'])
        st.metric("Personal Tasks", stats['personal_tasks'])

def main():
    print(f"DEBUG: === APP START ===")
    print(f"DEBUG: Session state keys: {list(st.session_state.keys())}")
    
    st.title("🎤 Voice Task Manager")
    st.markdown("Speak to manage your tasks - braindump, organize, and track!")
    
    whisper, llm, task_manager, command_router, tts_service, task_matcher = init_services()
    
    # Initialize session state
    if 'mode' not in st.session_state:
        st.session_state.mode = 'braindump'
        print(f"DEBUG: Initialized mode to braindump")
    if 'last_mode' not in st.session_state:
        st.session_state.last_mode = 'braindump'
        print(f"DEBUG: Initialized last_mode to braindump")
    if 'current_audio_hash' not in st.session_state:
        st.session_state.current_audio_hash = None
        print(f"DEBUG: Initialized current_audio_hash to None")
    if 'processed_tasks' not in st.session_state:
        st.session_state.processed_tasks = None
        print(f"DEBUG: Initialized processed_tasks to None")
    if 'transcription' not in st.session_state:
        st.session_state.transcription = None
        print(f"DEBUG: Initialized transcription to None")
    if 'last_command_result' not in st.session_state:
        st.session_state.last_command_result = None
        print(f"DEBUG: Initialized last_command_result to None")
    
    print(f"DEBUG: Current mode: {st.session_state.mode}")
    print(f"DEBUG: Current audio hash: {st.session_state.current_audio_hash}")
    print(f"DEBUG: Has processed tasks: {st.session_state.processed_tasks is not None}")
    print(f"DEBUG: Has transcription: {st.session_state.transcription is not None}")
    
    # Mode selector
    st.subheader("🎯 Mode Selection")
    mode = st.radio(
        "Choose your mode:",
        ["🧠 Brain Dump", "🎯 Command"],
        horizontal=True,
        index=0 if st.session_state.mode == 'braindump' else 1,
        key="mode_selector"
    )
    
    # Update session state
    new_mode = 'braindump' if mode == "🧠 Brain Dump" else 'command'
    print(f"DEBUG: Radio selection: {mode} -> new_mode: {new_mode}")
    
    if new_mode != st.session_state.mode:
        print(f"DEBUG: Mode changed from {st.session_state.mode} to {new_mode}")
        st.session_state.mode = new_mode
    
    # Clear audio state if mode changed
    if st.session_state.last_mode != st.session_state.mode:
        print(f"DEBUG: Mode changed, clearing audio state")
        st.session_state.processed_tasks = None
        st.session_state.transcription = None
        st.session_state.last_command_result = None
        st.session_state.last_mode = st.session_state.mode
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("🎤 Voice Input")
        
        # Mode-specific instructions
        if st.session_state.mode == 'braindump':
            st.info("🧠 **Brain Dump Mode**: Speak freely about multiple tasks and ideas. I'll extract and organize them for you.")
        else:
            st.info("🎯 **Command Mode**: Give specific commands like 'Add a task to review documentation' or 'Mark the first task as complete'.")
        
        print(f"DEBUG: About to show audio input widget")
        
        # Audio input
        audio_value = st.audio_input("Click to record your voice")
        
        print(f"DEBUG: Audio input widget returned: {audio_value is not None}")
        if audio_value:
            print(f"DEBUG: Audio value name: {audio_value.name}, size: {audio_value.size}")
        
        # Process audio only if we have new audio
        if audio_value:
            # Create hash of current audio
            current_hash = hash(str(audio_value.name) + str(audio_value.size))
            print(f"DEBUG: Current audio hash: {current_hash}")
            print(f"DEBUG: Stored audio hash: {st.session_state.current_audio_hash}")
            
            # Only process if this is new audio
            if current_hash != st.session_state.current_audio_hash:
                print(f"DEBUG: NEW AUDIO DETECTED - Processing audio")
                st.session_state.current_audio_hash = current_hash
                
                # Display the recorded audio
                st.audio(audio_value)
                
                # Get audio bytes from the UploadedFile object
                audio_bytes = audio_value.read()
                print(f"DEBUG: Audio bytes length: {len(audio_bytes)}")
                
                with st.spinner("Transcribing..."):
                    print(f"DEBUG: Starting transcription")
                    transcription = whisper.transcribe(audio_bytes)
                    print(f"DEBUG: Transcription result: {transcription}")
                    
                if transcription:
                    st.session_state.transcription = transcription
                    st.success("Transcribed!")
                    st.text_area("Raw Transcription:", transcription, height=100)
                    
                    # Process based on mode
                    if st.session_state.mode == 'braindump':
                        print(f"DEBUG: Processing in BRAIN DUMP mode")
                        with st.spinner("Processing brain dump..."):
                            processed_tasks = llm.process_braindump(transcription)
                            st.session_state.processed_tasks = processed_tasks
                            print(f"DEBUG: Processed tasks: {processed_tasks}")
                        
                        if processed_tasks:
                            st.info("AI Processed Tasks:")
                            for task in processed_tasks:
                                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get('priority', 'medium'), '⚪')
                                category_emoji = {"client": "👤", "business": "💼", "personal": "🏠"}.get(task.get('category'), '📝')
                                st.write(f"• {priority_emoji} {category_emoji} {task.get('text', task)}")
                    else:
                        print(f"DEBUG: Processing in COMMAND mode")
                        # Command mode
                        with st.spinner("Processing command..."):
                            current_tasks = task_manager.get_tasks()
                            result = command_router.process_command(transcription, 'command', current_tasks)
                            st.session_state.last_command_result = result
                            print(f"DEBUG: Command result: {result}")
                        
                        # Display command result
                        if result['action_taken']:
                            st.success(result['message'])
                            tts_service.speak_confirmation('task_updated' if result['intent'] == 'modify' else 'task_added')
                        elif result['intent'] == 'query':
                            st.info(result['message'])
                            tts_service.speak_query_response(result['message'])
                        else:
                            st.warning(result['message'])
                            if result['confidence'] < 0.7:
                                tts_service.speak_confirmation('low_confidence')
                        
                        # Show confidence score
                        st.metric("Confidence", f"{result['confidence']:.1%}")
                        
                        # Clear transcription but keep audio hash to prevent reprocessing
                        st.session_state.transcription = None
                        print(f"DEBUG: Cleared transcription after command processing")
            else:
                print(f"DEBUG: Audio hash unchanged - not processing")
        
        # Show action buttons if we have results
        if st.session_state.processed_tasks or st.session_state.last_command_result:
            print(f"DEBUG: Showing action buttons")
            
            # Add to Task List button for processed tasks
            if st.session_state.processed_tasks:
                if st.button("Add to Task List", key="add_tasks"):
                    print(f"DEBUG: Add to Task List button clicked")
                    for processed_task in st.session_state.processed_tasks:
                        if isinstance(processed_task, dict):
                            task_manager.add_task(
                                processed_task.get('text', ''),
                                priority=processed_task.get('priority', 'medium'),
                                category=processed_task.get('category')
                            )
                            print(f"DEBUG: Added task: {processed_task.get('text', '')}")
                        else:
                            # Fallback for string tasks
                            task_manager.add_task(processed_task, priority='medium', category=None)
                            print(f"DEBUG: Added string task: {processed_task}")
                    tts_service.speak_confirmation('task_added', f"Added {len(st.session_state.processed_tasks)} tasks")
                    st.success("Tasks added!")
                    # Clear the processed tasks after adding
                    st.session_state.processed_tasks = None
                    st.session_state.transcription = None
                    print(f"DEBUG: Cleared processed tasks after adding")
                    st.rerun()
            
            # Clear Results button
            if st.button("Clear Results", key="clear_results"):
                print(f"DEBUG: Clear Results button clicked")
                st.session_state.processed_tasks = None
                st.session_state.transcription = None
                st.session_state.last_command_result = None
                st.success("Results cleared!")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        col_clear, col_prioritize = st.columns(2)
        
        with col_clear:
            if st.button("Clear All Tasks", type="secondary"):
                print(f"DEBUG: Clear All Tasks button clicked")
                task_manager.clear_all()
                tts_service.speak_confirmation('tasks_cleared')
                st.success("All tasks cleared!")
                st.rerun()
        
        with col_prioritize:
            if st.button("Auto-Prioritize", type="secondary"):
                print(f"DEBUG: Auto-Prioritize button clicked")
                current_tasks = task_manager.get_tasks()
                updated_tasks = llm.prioritize_tasks(current_tasks)
                tts_service.speak_confirmation('task_updated', "Tasks prioritized")
                st.success("Tasks prioritized!")
    
    with col2:
        st.header("📋 Task List")
        
        tasks = task_manager.get_tasks()
        print(f"DEBUG: Retrieved {len(tasks)} tasks from task manager")
        
        if not tasks:
            st.info("No tasks yet. Start speaking to add some!")
        else:
            # Filter options
            st.subheader("🔍 Filters")
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                priority_filter = st.selectbox(
                    "Priority",
                    ["All", "High", "Medium", "Low"],
                    key="priority_filter"
                )
                print(f"DEBUG: Priority filter changed to: {priority_filter}")
            
            with col_filter2:
                category_filter = st.selectbox(
                    "Category",
                    ["All", "Client", "Business", "Personal"],
                    key="category_filter"
                )
                print(f"DEBUG: Category filter changed to: {category_filter}")
            
            with col_filter3:
                status_filter = st.selectbox(
                    "Status",
                    ["All", "Pending", "Completed"],
                    key="status_filter"
                )
                print(f"DEBUG: Status filter changed to: {status_filter}")
            
            # Apply filters
            filtered_tasks = tasks
            
            if priority_filter != "All":
                priority_lower = priority_filter.lower()
                filtered_tasks = [t for t in filtered_tasks if t.get('priority') == priority_lower]
            
            if category_filter != "All":
                category_lower = category_filter.lower()
                filtered_tasks = [t for t in filtered_tasks if t.get('category') == category_lower]
            
            if status_filter == "Pending":
                filtered_tasks = [t for t in filtered_tasks if not t['completed']]
            elif status_filter == "Completed":
                filtered_tasks = [t for t in filtered_tasks if t['completed']]
            
            print(f"DEBUG: After filtering: {len(filtered_tasks)} tasks")
            
            # Display filtered tasks
            if not filtered_tasks:
                st.info("No tasks match the current filters.")
            else:
                for task in filtered_tasks:
                    render_task(task, task_manager, tts_service)
                    st.divider()
        
        # Enhanced statistics
        if tasks:
            render_stats(task_manager.get_stats())
    
    print(f"DEBUG: === APP END ===")

if __name__ == "__main__":
    main()