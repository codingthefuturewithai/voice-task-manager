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
from services.help_service import HelpService

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
    
    # Try to initialize the agent service (optional enhancement)
    agent_service = None
    try:
        from services.agent_service import AgentService
        agent_service = AgentService(api_key, task_manager)
        print("✅ Agent service initialized successfully")
    except Exception as e:
        print(f"ℹ️ Agent service not available (optional): {e}")
        # Continue without agent - app works fine with existing functionality
    
    # Pass agent_service to HelpService (will use if available)
    help_service = HelpService(llm, agent_service)
    
    return whisper, llm, task_manager, command_router, tts_service, task_matcher, help_service

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
    
    # Callback functions that execute BEFORE rerun
    def start_edit():
        st.session_state[edit_key] = True
    
    def save_edit(task_id, new_text):
        task_manager.update_task(task_id, text=new_text)
        st.session_state[edit_key] = False
    
    def cancel_edit():
        st.session_state[edit_key] = False
    
    def toggle_complete(task_id):
        task_manager.toggle_task(task_id)
    
    def delete_task(task_id):
        task_manager.delete_task(task_id)
    
    col_check, col_priority, col_task, col_category, col_delete = st.columns([1, 1, 6, 1, 1])
    
    with col_check:
        # Use checkbox without callback, check for state change manually
        checkbox_key = f"check_{task['id']}"
        is_checked = st.checkbox("Done", value=task["completed"], key=checkbox_key, 
                                 label_visibility="hidden")
        
        # Only toggle if the state actually changed from what's in the database
        if is_checked != task["completed"]:
            task_manager.toggle_task(task['id'])
    
    with col_priority:
        priority_emoji = priority_colors.get(task.get('priority', 'medium'), '⚪')
        st.write(priority_emoji)
    
    with col_task:
        if st.session_state[edit_key]:
            # Edit mode
            new_text = st.text_input("Edit task:", value=task['text'], key=f"text_{task['id']}")
            col_save, col_cancel = st.columns(2)
            with col_save:
                st.button("💾", key=f"save_{task['id']}", on_click=save_edit, 
                         args=(task['id'], new_text))
            with col_cancel:
                st.button("❌", key=f"cancel_{task['id']}", on_click=cancel_edit)
        else:
            # Display mode
            if task["completed"]:
                st.markdown(f"~~{task['text']}~~")
            else:
                st.markdown(task['text'])
            
            # Edit button with callback
            st.button("✏️", key=f"edit_btn_{task['id']}", on_click=start_edit)
    
    with col_category:
        if task.get('category'):
            category_emoji = category_labels.get(task['category'], '📝')
            st.write(category_emoji)
        else:
            st.write("")
    
    with col_delete:
        st.button("🗑️", key=f"del_{task['id']}", on_click=delete_task, args=(task['id'],))

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
    
    whisper, llm, task_manager, command_router, tts_service, task_matcher, help_service = init_services()
    
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
    if 'help_panel_open' not in st.session_state:
        st.session_state.help_panel_open = False
        print(f"DEBUG: Initialized help_panel_open to False")
    if 'help_question' not in st.session_state:
        st.session_state.help_question = ""
        print(f"DEBUG: Initialized help_question to empty string")
    if 'help_response' not in st.session_state:
        st.session_state.help_response = ""
        print(f"DEBUG: Initialized help_response to empty string")
    if 'help_input_counter' not in st.session_state:
        st.session_state.help_input_counter = 0
        print(f"DEBUG: Initialized help_input_counter to 0")
    if 'last_help_question_processed' not in st.session_state:
        st.session_state.last_help_question_processed = None
        print(f"DEBUG: Initialized last_help_question_processed to None")
    if 'help_audio_version' not in st.session_state:
        st.session_state.help_audio_version = 0
        print(f"DEBUG: Initialized help_audio_version to 0")
    if 'help_mode' not in st.session_state:
        st.session_state.help_mode = 'question'  # 'question' or 'command'
        print(f"DEBUG: Initialized help_mode to question")
    
    print(f"DEBUG: Current mode: {st.session_state.mode}")
    print(f"DEBUG: Current audio hash: {st.session_state.current_audio_hash}")
    print(f"DEBUG: Has processed tasks: {st.session_state.processed_tasks is not None}")
    print(f"DEBUG: Has transcription: {st.session_state.transcription is not None}")
    
    # Help Panel in Sidebar - Clean, simple, reliable
    def render_help_panel():
        st.header("🤖 AI Assistant")
        
        # Help panel toggle
        help_status = "🟢 Active" if st.session_state.help_panel_open else "⚪ Inactive"
        if st.button(f"🔧 Toggle Panel ({help_status})", key="toggle_help"):
            st.session_state.help_panel_open = not st.session_state.help_panel_open
        
        # Help panel content
        if st.session_state.help_panel_open:
            st.divider()
            
            # Mode Toggle - Prominent at top
            st.markdown("### Select Mode")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❓ Question Mode" if st.session_state.help_mode != 'question' else "✅ Question Mode",
                    key="mode_question",
                    use_container_width=True,
                    type="primary" if st.session_state.help_mode == 'question' else "secondary"
                ):
                    st.session_state.help_mode = 'question'
                    st.session_state.help_response = ""  # Clear previous response
                    print(f"DEBUG: Switched to Question mode")
            
            with col2:
                if st.button(
                    "⚡ Command Mode" if st.session_state.help_mode != 'command' else "✅ Command Mode",
                    key="mode_command",
                    use_container_width=True,
                    type="primary" if st.session_state.help_mode == 'command' else "secondary"
                ):
                    st.session_state.help_mode = 'command'
                    st.session_state.help_response = ""  # Clear previous response
                    print(f"DEBUG: Switched to Command mode")
            
            # Mode description
            if st.session_state.help_mode == 'question':
                st.info("📚 Ask questions about how to use the app")
            else:
                st.success("🚀 I'll execute commands for you")
            
            st.divider()
            
            # Voice Input - PROMINENT AT TOP
            mode_text = "question" if st.session_state.help_mode == 'question' else "command"
            st.markdown(f"### 🎤 Speak your {mode_text}")
            help_audio = st.audio_input(
                "Click to record",
                key=f"help_audio_{st.session_state.help_audio_version}"
            )
            
            if help_audio:
                print(f"DEBUG: Help audio detected in {st.session_state.help_mode} mode")
                # Process help voice input
                help_audio_bytes = help_audio.read()
                help_transcription = whisper.transcribe(help_audio_bytes)
                
                if help_transcription and help_transcription != st.session_state.last_help_question_processed:
                    print(f"DEBUG: Help transcription: {help_transcription}")
                    st.session_state.help_question = help_transcription
                    st.session_state.last_help_question_processed = help_transcription
                    
                    # Process based on mode
                    current_tasks = task_manager.get_tasks()
                    with st.spinner("Processing..."):
                        # Pass mode to help service
                        help_response = help_service.get_help_response(
                            help_transcription, 
                            current_tasks,
                            mode=st.session_state.help_mode
                        )
                        st.session_state.help_response = help_response
                        print(f"DEBUG: Help response generated from voice: {len(help_response)} characters")
                    
                    # Check if tasks were updated (command mode)
                    if 'tasks_updated' in st.session_state and st.session_state.tasks_updated:
                        print(f"DEBUG: Tasks were updated, triggering rerun")
                        st.session_state.tasks_updated = False
                    else:
                        print(f"DEBUG: Response ready, triggering rerun to display")
                    
                    # Increment audio version to reset the widget
                    st.session_state.help_audio_version += 1
                    print(f"DEBUG: Incremented help_audio_version to {st.session_state.help_audio_version}")
                    st.rerun()
            
            # Text input (secondary option) in a form
            with st.form(key="help_text_form", clear_on_submit=True):
                help_text = st.text_input(
                    f"Or type your {mode_text}:",
                    placeholder="Add a task to buy groceries" if st.session_state.help_mode == 'command' 
                               else "How do I add a task?"
                )
                submitted = st.form_submit_button("Submit", use_container_width=True)
                
                if submitted and help_text and help_text.strip():
                    print(f"DEBUG: Text submitted in {st.session_state.help_mode} mode: {help_text}")
                    st.session_state.help_question = help_text
                    st.session_state.last_help_question_processed = help_text
                    
                    # Process based on mode
                    current_tasks = task_manager.get_tasks()
                    help_response = help_service.get_help_response(
                        help_text,
                        current_tasks,
                        mode=st.session_state.help_mode
                    )
                    st.session_state.help_response = help_response
                    print(f"DEBUG: Help response generated: {len(help_response)} characters")
                    
                    # Check if tasks were updated
                    if 'tasks_updated' in st.session_state and st.session_state.tasks_updated:
                        print(f"DEBUG: Tasks were updated, triggering full rerun")
                        st.session_state.tasks_updated = False
                    st.rerun()
            
            # Response Area - FIXED AT BOTTOM
            st.divider()
            
            # Always show transcription if available
            if st.session_state.help_question:
                st.markdown("**Transcribed/Input:**")
                st.code(st.session_state.help_question)
            
            if st.session_state.help_response:
                # Show response
                st.markdown("**Response:**")
                st.markdown(st.session_state.help_response)
                
                # Single clear button
                if st.button("Clear", key="clear_response"):
                    st.session_state.help_response = ""
                    st.session_state.help_question = ""
                    st.session_state.help_audio_version += 1
                    st.rerun()
            else:
                mode_label = "question" if st.session_state.help_mode == 'question' else "command"
                st.info(f"💭 Ready for your {mode_label}...")
    
    # Call the help panel in the sidebar
    with st.sidebar:
        render_help_panel()
    
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