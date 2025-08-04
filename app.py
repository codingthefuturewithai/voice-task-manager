import streamlit as st
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from pathlib import Path

from services.whisper_service import WhisperService
from services.llm_service import LLMService
from services.task_manager import TaskManager

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
    return whisper, llm, task_manager

def main():
    st.title("🎤 Voice Task Manager")
    st.markdown("Speak to manage your tasks - braindump, organize, and track!")
    
    whisper, llm, task_manager = init_services()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Voice Input")
        
        audio_value = st.audio_input("Click to record your brain dump")
        
        if audio_value:
            # Display the recorded audio
            st.audio(audio_value)
            
            # Get audio bytes from the UploadedFile object
            audio_bytes = audio_value.read()
            
            with st.spinner("Transcribing..."):
                transcription = whisper.transcribe(audio_bytes)
                
            if transcription:
                st.success("Transcribed!")
                st.text_area("Raw Transcription:", transcription, height=100)
                
                with st.spinner("Processing with AI..."):
                    processed_tasks = llm.process_braindump(transcription)
                
                if processed_tasks:
                    st.info("AI Processed Tasks:")
                    for task in processed_tasks:
                        st.write(f"• {task}")
                    
                    if st.button("Add to Task List"):
                        for task in processed_tasks:
                            task_manager.add_task(task)
                        st.success("Tasks added!")
                        st.rerun()
        
        st.divider()
        
        if st.button("Clear All Tasks", type="secondary"):
            task_manager.clear_all()
            st.success("All tasks cleared!")
            st.rerun()
    
    with col2:
        st.header("Task List")
        
        tasks = task_manager.get_tasks()
        
        if not tasks:
            st.info("No tasks yet. Start speaking to add some!")
        else:
            for idx, task in enumerate(tasks):
                col_check, col_task, col_delete = st.columns([1, 8, 1])
                
                with col_check:
                    if st.checkbox("", value=task["completed"], key=f"check_{task['id']}"):
                        task_manager.toggle_task(task['id'])
                        st.rerun()
                
                with col_task:
                    if task["completed"]:
                        st.markdown(f"~~{task['text']}~~")
                    else:
                        st.markdown(task['text'])
                
                with col_delete:
                    if st.button("🗑️", key=f"del_{task['id']}"):
                        task_manager.delete_task(task['id'])
                        st.rerun()
        
        st.divider()
        stats = task_manager.get_stats()
        st.metric("Total Tasks", stats['total'])
        col_a, col_b = st.columns(2)
        col_a.metric("Completed", stats['completed'])
        col_b.metric("Pending", stats['pending'])

if __name__ == "__main__":
    main()