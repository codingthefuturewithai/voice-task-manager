from typing import Dict, Any, Optional, List
import os
from pathlib import Path
import json

class HelpService:
    def __init__(self, llm_service):
        """
        Initialize the help service with access to the LLM service
        
        Args:
            llm_service: The existing LLMService instance
        """
        self.llm_service = llm_service
        self.knowledge_base = self._load_knowledge_base()
        self.ui_reference = self._load_ui_reference()
    
    def _load_knowledge_base(self) -> str:
        """
        Load the help knowledge base from the markdown file
        """
        try:
            knowledge_path = Path(__file__).parent.parent / "help_knowledge.md"
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print("Warning: help_knowledge.md not found, using fallback knowledge")
            return self._get_fallback_knowledge()
    
    def _load_ui_reference(self) -> dict:
        """
        Load the UI elements reference from the JSON file
        """
        try:
            ref_path = Path(__file__).parent.parent / ".reference" / "ui_elements.json"
            with open(ref_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: ui_elements.json not found")
            return {}
    
    def _get_fallback_knowledge(self) -> str:
        """
        Fallback knowledge base if the markdown file is not found
        """
        return """
        # Voice Task Manager Help
        
        ## Modes
        - Brain Dump Mode: Extract multiple tasks from free-form speech
        - Command Mode: Execute specific actions on tasks
        
        ## Common Commands
        - "Add a task to [description]"
        - "Mark [task] as complete"
        - "Show me all [priority] priority tasks"
        - "Delete [task]"
        
        ## Task Properties
        - Priorities: High (🔴), Medium (🟡), Low (🟢)
        - Categories: Client (👤), Business (💼), Personal (🏠)
        """
    
    def get_help_response(self, user_question: str, current_tasks: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Get a helpful response to a user's question using the LLM and knowledge base
        
        Args:
            user_question: The user's question or request for help
            current_tasks: Optional list of current tasks for context-aware help
            
        Returns:
            A helpful response string
        """
        try:
            # Build context with knowledge base and UI reference
            ui_ref_str = json.dumps(self.ui_reference, indent=2) if self.ui_reference else ""
            
            context = f"""
            You are a helpful assistant for the Voice Task Manager application. 
            Use the following knowledge base to answer user questions:
            
            {self.knowledge_base}
            
            UI Elements Reference (for precise location answers):
            {ui_ref_str}
            
            Current application state:
            - Total tasks: {len(current_tasks) if current_tasks else 0}
            """
            
            # Add task context if available
            if current_tasks:
                pending_tasks = [t for t in current_tasks if not t.get('completed', False)]
                high_priority_tasks = [t for t in pending_tasks if t.get('priority') == 'high']
                client_tasks = [t for t in current_tasks if t.get('category') == 'client']
                business_tasks = [t for t in current_tasks if t.get('category') == 'business']
                personal_tasks = [t for t in current_tasks if t.get('category') == 'personal']
                
                context += f"""
                - Pending tasks: {len(pending_tasks)}
                - High priority tasks: {len(high_priority_tasks)}
                - Client tasks: {len(client_tasks)}
                - Business tasks: {len(business_tasks)}
                - Personal tasks: {len(personal_tasks)}
                """
                
                if high_priority_tasks:
                    context += "\nHigh priority tasks:\n"
                    for i, task in enumerate(high_priority_tasks[:3], 1):
                        context += f"- {i}. {task.get('text', 'Unknown task')}\n"
            
            # Create the prompt
            prompt = f"""
            {context}
            
            User Question: "{user_question}"
            
            Provide a helpful, friendly response that:
            1. Directly answers their question
            2. Uses the knowledge base information
            3. Provides specific examples when helpful
            4. Suggests relevant voice commands they could try
            5. Keeps the response concise but informative
            
            If they have high priority tasks, consider mentioning them.
            If they're asking about commands, provide specific examples they can say.
            """
            
            # Use the LLM service to generate response
            response = self.llm_service.client.chat.completions.create(
                model=self.llm_service.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Voice Task Manager assistant. Provide clear, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Help service error: {e}")
            return "I'm having trouble accessing the help system right now. Please try again or check the knowledge base documentation."
    
    def get_contextual_suggestions(self, current_tasks: List[Dict[str, Any]]) -> str:
        """
        Get contextual suggestions based on current task state
        
        Args:
            current_tasks: List of current tasks
            
        Returns:
            A string with contextual suggestions
        """
        try:
            if not current_tasks:
                return "You have no tasks yet! Try saying 'Add a task to review documentation' or use Brain Dump mode to add multiple tasks at once."
            
            pending_tasks = [t for t in current_tasks if not t.get('completed', False)]
            high_priority_tasks = [t for t in pending_tasks if t.get('priority') == 'high']
            
            if high_priority_tasks:
                suggestions = f"You have {len(high_priority_tasks)} high-priority tasks. Try saying:\n"
                suggestions += "• 'Mark the first task as complete'\n"
                suggestions += "• 'Show me all high priority tasks'\n"
                suggestions += "• 'What should I work on next?'"
            elif pending_tasks:
                suggestions = f"You have {len(pending_tasks)} pending tasks. Try saying:\n"
                suggestions += "• 'Mark the first task as complete'\n"
                suggestions += "• 'Show me all client tasks'\n"
                suggestions += "• 'Auto-prioritize my tasks'"
            else:
                suggestions = "All your tasks are complete! Great job! Try adding new tasks with Brain Dump mode."
            
            return suggestions
            
        except Exception as e:
            print(f"Contextual suggestions error: {e}")
            return "Try saying 'Add a task' or 'Show me my tasks' to get started."
    
    def get_quick_reference(self) -> str:
        """
        Get a quick reference guide for common commands
        
        Returns:
            A formatted quick reference string
        """
        return """
        **Quick Reference - Voice Commands**
        
        **Adding Tasks:**
        • "Add a task to [description]"
        • "Create a task for [description]"
        
        **Managing Tasks:**
        • "Mark [task] as complete"
        • "Mark the first task as done"
        • "Change priority to high"
        • "Move task to client category"
        
        **Querying:**
        • "Show me all high priority tasks"
        • "What are my client tasks?"
        • "How many tasks do I have?"
        
        **Deleting:**
        • "Delete [task description]"
        • "Remove the third task"
        """ 