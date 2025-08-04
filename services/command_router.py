from typing import Dict, Any, List, Optional
from services.llm_service import LLMService
from services.task_manager import TaskManager

class CommandRouter:
    def __init__(self, llm_service: LLMService, task_manager: TaskManager):
        self.llm = llm_service
        self.tasks = task_manager
    
    def process_command(self, transcription: str, mode: str, current_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Route transcribed text to appropriate handler based on mode and intent
        Returns: {
            'intent': 'add|modify|delete|query|prioritize|braindump',
            'confidence': float,
            'target_task': dict or None,
            'new_content': str or None,
            'priority': str or None,
            'category': str or None,
            'tasks': list,  # for braindump mode
            'message': str,  # user-friendly message
            'action_taken': bool
        }
        """
        try:
            # Detect intent using LLM
            intent_result = self.llm.detect_intent(transcription, current_tasks)
            
            intent = intent_result.get('intent', 'braindump')
            confidence = intent_result.get('confidence', 0.5)
            target_task_id = intent_result.get('target_task_id')
            new_content = intent_result.get('new_content')
            priority = intent_result.get('priority', 'medium')
            category = intent_result.get('category')
            
            # Find target task if ID provided
            target_task = None
            if target_task_id:
                for task in current_tasks:
                    if task['id'] == target_task_id:
                        target_task = task
                        break
            
            # If no target task found but intent suggests we need one, try fuzzy matching
            if not target_task and intent in ['modify', 'delete', 'complete']:
                target_task = self.llm.match_task(transcription, current_tasks)
            
            # Handle different intents
            action_taken = False
            message = ""
            
            if intent == 'add' and new_content:
                # Add new task
                task_id = self.tasks.add_task(new_content, priority, category)
                action_taken = True
                message = f"Added task: {new_content}"
                
            elif intent == 'modify' and target_task and new_content:
                # Modify existing task
                self.tasks.update_task(target_task['id'], text=new_content)
                if priority != 'medium':
                    self.tasks.update_task(target_task['id'], priority=priority)
                if category:
                    self.tasks.update_task(target_task['id'], category=category)
                action_taken = True
                message = f"Updated task: {new_content}"
                
            elif intent == 'delete' and target_task:
                # Delete task
                task_text = target_task['text']
                self.tasks.delete_task(target_task['id'])
                action_taken = True
                message = f"Deleted task: {task_text}"
                
            elif intent == 'complete' and target_task:
                # Mark task as complete
                self.tasks.update_task(target_task['id'], completed=True)
                action_taken = True
                message = f"Completed task: {target_task['text']}"
                
            elif intent == 'query':
                # Handle queries
                if 'next' in transcription.lower() or 'work on' in transcription.lower():
                    suggested_task = self.llm.suggest_next_task(current_tasks)
                    if suggested_task:
                        message = f"You should work on: {suggested_task['text']} (Priority: {suggested_task['priority']})"
                    else:
                        message = "No pending tasks to work on!"
                elif 'client' in transcription.lower():
                    client_tasks = self.tasks.get_tasks_by_category('client')
                    if client_tasks:
                        task_list = "\n".join([f"• {t['text']}" for t in client_tasks])
                        message = f"Client tasks:\n{task_list}"
                    else:
                        message = "No client tasks found."
                elif 'priority' in transcription.lower():
                    high_tasks = self.tasks.get_tasks_by_priority('high')
                    if high_tasks:
                        task_list = "\n".join([f"• {t['text']}" for t in high_tasks])
                        message = f"High priority tasks:\n{task_list}"
                    else:
                        message = "No high priority tasks found."
                else:
                    message = f"Query: {transcription}"
                    
            elif intent == 'prioritize':
                # Prioritize tasks
                updated_tasks = self.llm.prioritize_tasks(current_tasks)
                action_taken = True
                message = "Tasks have been prioritized based on content analysis."
                
            elif intent == 'braindump' or mode == 'braindump':
                # Process as brain dump
                processed_tasks = self.llm.process_braindump(transcription)
                if processed_tasks:
                    for task in processed_tasks:
                        self.tasks.add_task(task, priority, category)
                    action_taken = True
                    message = f"Added {len(processed_tasks)} tasks from brain dump"
                else:
                    message = "No tasks extracted from brain dump"
            
            # If confidence is low, provide fallback options
            if confidence < 0.7 and not action_taken:
                message = f"Low confidence ({confidence:.1%}) in understanding: '{transcription}'. Please try rephrasing."
            
            return {
                'intent': intent,
                'confidence': confidence,
                'target_task': target_task,
                'new_content': new_content,
                'priority': priority,
                'category': category,
                'tasks': processed_tasks if intent == 'braindump' else [],
                'message': message,
                'action_taken': action_taken
            }
            
        except Exception as e:
            print(f"Command routing error: {e}")
            return {
                'intent': 'error',
                'confidence': 0.0,
                'target_task': None,
                'new_content': None,
                'priority': None,
                'category': None,
                'tasks': [],
                'message': f"Error processing command: {str(e)}",
                'action_taken': False
            } 