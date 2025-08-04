import streamlit as st
from typing import Optional

class TTSService:
    def __init__(self, method: str = 'browser'):
        """
        Initialize TTS service
        method: 'browser' for browser-native speech synthesis (recommended)
        """
        self.method = method
    
    def speak(self, text: str, rate: float = 1.2, pitch: float = 1.0):
        """
        Speak text using the configured method
        """
        if not text:
            return
        
        if self.method == 'browser':
            self._speak_browser(text, rate, pitch)
        else:
            # Fallback to just displaying the text
            st.info(f"Voice feedback: {text}")
    
    def _speak_browser(self, text: str, rate: float = 1.2, pitch: float = 1.0):
        """
        Use browser-native speech synthesis
        """
        # Escape quotes in text to prevent JavaScript errors
        safe_text = text.replace('"', '\\"').replace("'", "\\'")
        
        # Create JavaScript to trigger speech synthesis
        js_code = f"""
        <script>
        if ('speechSynthesis' in window) {{
            const utterance = new SpeechSynthesisUtterance("{safe_text}");
            utterance.rate = {rate};
            utterance.pitch = {pitch};
            utterance.volume = 0.8;
            window.speechSynthesis.speak(utterance);
        }} else {{
            console.log('Speech synthesis not supported');
        }}
        </script>
        """
        
        # Use Streamlit components to inject JavaScript
        st.components.v1.html(js_code, height=0)
    
    def speak_confirmation(self, action: str, details: Optional[str] = None):
        """
        Speak a confirmation message for common actions
        """
        try:
            if action == 'task_added':
                message = f"Task added successfully"
            elif action == 'task_updated':
                message = f"Task updated successfully"
            elif action == 'task_deleted':
                message = f"Task deleted successfully"
            elif action == 'task_completed':
                message = f"Task marked as complete"
            elif action == 'tasks_cleared':
                message = f"All tasks cleared"
            elif action == 'low_confidence':
                message = f"I'm not sure what you meant. Please try again"
            else:
                message = action
            
            if details:
                message += f". {details}"
            
            self.speak(message)
        except Exception as e:
            print(f"TTS error: {e}")
            # Fallback to just displaying the message
            st.info(f"Voice feedback: {message}")
    
    def speak_query_response(self, response: str):
        """
        Speak a response to a query
        """
        self.speak(response)
    
    def speak_error(self, error_message: str):
        """
        Speak an error message
        """
        self.speak(f"Error: {error_message}") 