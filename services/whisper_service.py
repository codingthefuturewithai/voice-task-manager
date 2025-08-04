from openai import OpenAI
import tempfile
import os

class WhisperService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio bytes using OpenAI Whisper API
        """
        try:
            # Save audio bytes to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            # Transcribe using Whisper
            with open(tmp_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            return transcript
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return None