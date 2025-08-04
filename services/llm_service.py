from openai import OpenAI
from typing import List, Dict, Any, Optional
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
    
    def detect_intent(self, transcription: str, current_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detect user intent from voice command
        """
        try:
            # Convert tasks to JSON for context
            tasks_json = json.dumps(current_tasks, indent=2)
            
            prompt = f"""
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
            - braindump: User is doing a general brain dump (multiple tasks)

            Also identify:
            - Which task they're referring to (if applicable) - return the task ID
            - New content (for add/modify)
            - Priority level mentioned (high/medium/low)
            - Category mentioned (client/business/personal)

            Return JSON only:
            {{
                "intent": "...",
                "confidence": 0.0-1.0,
                "target_task_id": "..." or null,
                "new_content": "..." or null,
                "priority": "..." or null,
                "category": "..." or null
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a task management assistant that analyzes voice commands."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            return json.loads(result)
            
        except Exception as e:
            print(f"Intent detection error: {e}")
            # Fallback: treat as braindump
            return {
                "intent": "braindump",
                "confidence": 0.5,
                "target_task_id": None,
                "new_content": None,
                "priority": None,
                "category": None
            }
    
    def match_task(self, query: str, tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Find task by natural language description
        """
        try:
            if not tasks:
                return None
            
            # Create a simple task list for matching
            task_list = []
            for task in tasks:
                task_list.append(f"ID: {task['id']}, Text: {task['text']}")
            
            task_text = "\n".join(task_list)
            
            prompt = f"""
            Find the task that best matches this description: "{query}"

            Available tasks:
            {task_text}

            Return ONLY the task ID that best matches, or "null" if no good match found.
            Example: "123e4567-e89b-12d3-a456-426614174000"
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a task matching assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            result = response.choices[0].message.content.strip()
            
            # Find the task by ID
            for task in tasks:
                if task['id'] in result:
                    return task
            
            return None
            
        except Exception as e:
            print(f"Task matching error: {e}")
            return None
    
    def suggest_next_task(self, tasks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Suggest what task to work on next
        """
        try:
            pending_tasks = [t for t in tasks if not t['completed']]
            if not pending_tasks:
                return None
            
            # Create task list with priorities
            task_list = []
            for task in pending_tasks:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task['priority'], "⚪")
                task_list.append(f"{priority_emoji} {task['text']} (Priority: {task['priority']})")
            
            task_text = "\n".join(task_list)
            
            prompt = f"""
            Based on these pending tasks, suggest which one the user should work on next.
            Consider priority levels and task content.

            Pending tasks:
            {task_text}

            Return ONLY the task text that should be worked on next.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a task prioritization assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            result = response.choices[0].message.content.strip()
            
            # Find the matching task
            for task in pending_tasks:
                if task['text'].lower() in result.lower() or result.lower() in task['text'].lower():
                    return task
            
            # Fallback to highest priority task
            priority_order = {'high': 3, 'medium': 2, 'low': 1}
            return max(pending_tasks, key=lambda t: priority_order.get(t['priority'], 0))
            
        except Exception as e:
            print(f"Task suggestion error: {e}")
            return None
    
    def prioritize_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Suggest task priorities based on content
        """
        try:
            pending_tasks = [t for t in tasks if not t['completed']]
            if not pending_tasks:
                return tasks
            
            task_list = []
            for task in pending_tasks:
                task_list.append(f"ID: {task['id']}, Text: {task['text']}, Current Priority: {task['priority']}")
            
            task_text = "\n".join(task_list)
            
            prompt = f"""
            Analyze these tasks and suggest appropriate priority levels (high/medium/low) based on:
            - Urgency and deadlines
            - Business impact
            - Dependencies
            - Effort required

            Tasks:
            {task_text}

            Return JSON array with task IDs and suggested priorities:
            [
                {{"id": "task_id", "priority": "high/medium/low"}},
                ...
            ]
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a task prioritization assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            suggestions = json.loads(result)
            
            # Apply suggestions
            for suggestion in suggestions:
                for task in tasks:
                    if task['id'] == suggestion['id']:
                        task['priority'] = suggestion['priority']
                        break
            
            return tasks
            
        except Exception as e:
            print(f"Task prioritization error: {e}")
            return tasks