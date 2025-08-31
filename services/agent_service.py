"""
LangGraph Agent Service with Direct Tool Integration
This service provides a modular agent using direct LangChain tools
while maintaining compatibility with the existing app architecture.
"""

from typing import Dict, Any, Optional
import asyncio
import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

class AgentService:
    """
    A modular agent service that uses direct LangChain tools.
    This runs alongside the existing LLMService without breaking current functionality.
    """
    
    def __init__(self, api_key: str, task_manager):
        """
        Initialize the agent service with direct LangChain tools.
        
        Args:
            api_key: OpenAI API key
            task_manager: Task manager instance for performing actions
        """
        self.api_key = api_key
        self.task_manager = task_manager
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            temperature=0.3
        )
        
        # Create tools directly
        self.tools = self._create_tools()
        
        # Create the agent with tools
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            prompt="""You are a Voice Task Manager assistant that executes actions directly.

You MUST use tools to execute ALL task-related commands.
NEVER explain how to do something - just DO IT using tools.

Examples:
- "Add task buy milk" → USE add_task tool
- "Mark buy groceries complete" → USE complete_task tool  
- "Complete the church task" → USE complete_task tool
- "I finished buy milk" → USE complete_task tool
- "Done with groceries" → USE complete_task tool

The ONLY time you explain without using tools is when user asks:
- "How do I..." 
- "What commands..."

Otherwise, ALWAYS execute the action with the appropriate tool."""
        )
    
    def _create_tools(self):
        """
        Create LangChain tools for task management.
        """
        # Reference to task_manager for use in tool functions
        task_manager = self.task_manager
        
        @tool
        def add_task(text: str, priority: str = "medium", category: Optional[str] = None) -> str:
            """
            Add a new task to the task list.
            
            IMPORTANT: The 'text' parameter should be the actual task content, not command words.
            
            Examples of correct usage:
            - User says "Add a task to buy milk" → add_task(text="buy milk")
            - User says "Create task for calling dentist" → add_task(text="calling dentist")
            - User says "Add new task buy pepsi cola" → add_task(text="buy pepsi cola")
            - User says "New high priority task review contract" → add_task(text="review contract", priority="high")
            
            Args:
                text: The actual task description (what needs to be done)
                priority: Task priority (high, medium, low)
                category: Optional category (client, business, personal)
            
            Returns:
                Confirmation message with the created task ID
            """
            try:
                # Validate inputs
                if not text or not text.strip():
                    return "Error: Task text cannot be empty"
                
                if priority not in ["high", "medium", "low"]:
                    priority = "medium"
                
                if category and category not in ["client", "business", "personal"]:
                    category = None
                
                # Add the task using the TaskManager
                task_id = task_manager.add_task(
                    text=text.strip(),
                    priority=priority,
                    category=category
                )
                
                # Trigger Streamlit UI refresh
                # Note: st.rerun() will be called from the help_service after getting the response
                
                # Return success message
                category_str = f" in {category} category" if category else ""
                return f"✅ Successfully added task: '{text}' with {priority} priority{category_str}"
                
            except Exception as e:
                return f"Error adding task: {str(e)}"
        
        @tool
        def complete_task(task_identifier: str) -> str:
            """
            Mark a task as completed by finding the best match.
            
            IMPORTANT: The 'task_identifier' should be the task content/description, not command words.
            
            Common phrases that trigger this tool:
            - "Mark X as done/complete"
            - "Complete X"
            - "I finished X"
            - "Check off X"
            - "Done with X"
            - "X is done"
            - "Cross off X"
            
            Examples of correct usage:
            - User says "Mark go to church as done" → complete_task(task_identifier="go to church")
            - User says "Complete the groceries task" → complete_task(task_identifier="groceries")
            - User says "I finished the equity agreement" → complete_task(task_identifier="equity agreement")
            - User says "Check off buy milk" → complete_task(task_identifier="buy milk")
            - User says "Done with calling the dentist" → complete_task(task_identifier="calling the dentist")
            
            Args:
                task_identifier: The task description or key words to identify which task to complete
            
            Returns:
                Success message if task was found and marked complete,
                or an error message with list of pending tasks if no match found
            """
            try:
                tasks = task_manager.get_tasks()
                pending_tasks = [t for t in tasks if not t.get('completed', False)]
                
                if not pending_tasks:
                    return "❌ No pending tasks to complete."
                
                # Normalize the identifier
                identifier_lower = task_identifier.lower().strip()
                
                # Try exact match first
                for task in pending_tasks:
                    if task['text'].lower().strip() == identifier_lower:
                        task_manager.toggle_task(task['id'])
                        return f"✅ Completed: {task['text']}"
                
                # Try substring match
                for task in pending_tasks:
                    task_text_lower = task['text'].lower()
                    # Check if identifier is in task or task is in identifier
                    if identifier_lower in task_text_lower or task_text_lower in identifier_lower:
                        task_manager.toggle_task(task['id'])
                        return f"✅ Completed: {task['text']}"
                
                # Try word-based matching
                identifier_words = set(identifier_lower.split())
                best_match = None
                best_score = 0
                
                for task in pending_tasks:
                    task_words = set(task['text'].lower().split())
                    common_words = identifier_words & task_words
                    score = len(common_words)
                    
                    if score > best_score and score >= 1:  # At least 1 word must match
                        best_score = score
                        best_match = task
                
                if best_match:
                    task_manager.toggle_task(best_match['id'])
                    return f"✅ Completed: {best_match['text']}"
                
                # No match found
                task_list = '\n'.join([f"- {t['text']}" for t in pending_tasks[:5]])
                return f"❌ Could not find a task matching '{task_identifier}'.\n\nYour pending tasks:\n{task_list}"
                
            except Exception as e:
                return f"Error completing task: {str(e)}"
        
        # Return list of tools
        return [add_task, complete_task]
    
    async def process_request(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a user request through the agent.
        
        Args:
            user_input: The user's input/question
            context: Optional context (current tasks, etc.)
        
        Returns:
            Dict with response and any tool results
        """
        try:
            # Just send the user input directly - no extra prompting
            print(f"DEBUG: Agent processing: '{user_input}'")
            
            # Invoke the agent
            result = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            print(f"DEBUG: Agent result: {result}")
            
            # Extract the response and tool calls
            tool_calls = []
            tool_responses = []
            ai_responses = []
            
            for message in result["messages"]:
                # Check message type
                msg_type = getattr(message, 'type', None)
                
                if msg_type == 'tool':
                    # This is a tool response (ToolMessage)
                    tool_responses.append(message.content)
                elif msg_type == 'ai':
                    # This is an AI message
                    # Check if it has tool calls
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        tool_calls.extend(message.tool_calls)
                    # Only add AI content if no tools were called yet
                    if message.content and not tool_calls:
                        ai_responses.append(message.content)
            
            # If tools were called, show only the tool response
            # This ignores the AI's post-tool commentary
            if tool_responses:
                response = "\n".join(tool_responses)
            else:
                # No tools called, show the AI's response
                response = "\n".join(ai_responses)
            
            return {
                "success": True,
                "response": response.strip(),
                "tool_calls": tool_calls
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": f"I encountered an error: {str(e)}"
            }
    
    def process_request_sync(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Synchronous wrapper for process_request (for Streamlit compatibility).
        
        Args:
            user_input: The user's input/question
            context: Optional context (current tasks, etc.)
        
        Returns:
            Dict with response and metadata
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.process_request(user_input, context))
        finally:
            loop.close()