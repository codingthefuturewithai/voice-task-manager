from openai import OpenAI
from typing import List
import json

class LLMService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cost-effective model
    
    def process_braindump(self, raw_text: str) -> List[str]:
        """
        Process raw braindump text into organized, actionable tasks
        """
        try:
            prompt = """
            You are a task organization assistant. Convert the following brain dump into a clean, organized list of actionable tasks.
            
            Rules:
            - Extract clear, actionable tasks
            - Remove filler words and make tasks concise
            - Group related items if appropriate
            - Each task should be self-contained and clear
            - Return as a JSON array of strings
            
            Brain dump:
            {text}
            
            Return ONLY a JSON array of task strings, no additional text.
            Example: ["Task 1", "Task 2", "Task 3"]
            """.format(text=raw_text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful task organization assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            tasks = json.loads(result)
            return tasks if isinstance(tasks, list) else []
            
        except Exception as e:
            print(f"LLM processing error: {e}")
            # Fallback: return the raw text as a single task
            return [raw_text] if raw_text else []