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
            model="gpt-5-nano",  # GPT-5 nano: 3x cheaper than GPT-4o-mini, 3x more context
            api_key=api_key
        )
        
        # Create tools directly
        self.tools = self._create_tools()
        
        # Store prompt for logging
        self.system_prompt = """You are a task management assistant.

When users request actions, use the available tools to complete them.
If you need information to complete a request, use tools to gather it first.

Always execute actions rather than explaining how to do them."""
        
        # Create the agent with tools
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            prompt=self.system_prompt
        )
    
    def _create_tools(self):
        """
        Create LangChain tools for task management.
        """
        # Reference to task_manager for use in tool functions
        task_manager = self.task_manager
        
        @tool
        def list_tasks(show_completed: bool = False) -> str:
            """
            List all tasks in the system.
            
            Args:
                show_completed: Whether to include completed tasks (default: False, only shows pending)
            
            Returns:
                A formatted list of tasks with their status
            """
            print(f"\n{'='*50}")
            print(f"LIST_TASKS TOOL CALLED BY LLM")
            print(f"show_completed: {show_completed}")
            print(f"{'='*50}\n")
            
            tasks = task_manager.get_tasks()
            
            if show_completed:
                task_list = tasks
            else:
                task_list = [t for t in tasks if not t.get('completed', False)]
            
            if not task_list:
                return "No tasks found."
            
            result = "Tasks:\n"
            for task in task_list:
                status = "✅" if task.get('completed', False) else "⬜"
                priority = task.get('priority', 'medium')
                result += f"{status} {task['text']} (Priority: {priority})\n"
            
            return result
        
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
            print(f"\n{'='*50}")
            print(f"ADD_TASK TOOL CALLED BY LLM")
            print(f"Received parameters from LLM:")
            print(f"  - text: '{text}'")
            print(f"  - priority: '{priority}'")
            print(f"  - category: '{category}'")
            print(f"{'='*50}\n")
            
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
                
                print(f"TASK ADDED SUCCESSFULLY: ID={task_id}")
                
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
            Mark an existing task as completed.
            
            Args:
                task_identifier: The EXACT text of the task to mark as complete
            
            Returns:
                Success message if task was marked complete, or error if not found
            """
            print(f"\n{'='*50}")
            print(f"COMPLETE_TASK TOOL CALLED BY LLM")
            print(f"Received task to complete: '{task_identifier}'")
            print(f"{'='*50}\n")
            
            try:
                tasks = task_manager.get_tasks()
                
                # Find exact match
                for task in tasks:
                    if task['text'].lower() == task_identifier.lower() and not task.get('completed', False):
                        print(f"FOUND TASK: '{task['text']}' (ID: {task['id']})")
                        print(f"MARKING TASK AS COMPLETE...")
                        task_manager.toggle_task(task['id'])
                        print(f"SUCCESS! Task marked as complete.")
                        return f"✅ Completed: {task['text']}"
                
                # No exact match found
                pending_tasks = [t for t in tasks if not t.get('completed', False)]
                print(f"NO EXACT MATCH for '{task_identifier}'")
                print(f"Available tasks: {[t['text'] for t in pending_tasks]}")
                
                if not pending_tasks:
                    return "❌ No pending tasks to complete."
                
                task_list = '\n'.join([f"- {t['text']}" for t in pending_tasks[:5]])
                return f"❌ Could not find task '{task_identifier}'.\n\nYour pending tasks:\n{task_list}"
                
            except Exception as e:
                print(f"EXCEPTION IN COMPLETE_TASK: {str(e)}")
                import traceback
                traceback.print_exc()
                return f"Error completing task: {str(e)}"
        
        # Return list of tools
        return [list_tasks, add_task, complete_task]
    
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
            # Log the complete system prompt
            print(f"\n{'='*100}")
            print(f"!!! AGENT SERVICE - PROCESSING USER REQUEST !!!")
            print(f"USER INPUT: '{user_input}'")
            print(f"AVAILABLE TOOLS FOR LLM TO CALL: {[tool.name for tool in self.tools]}")
            print(f"\nSYSTEM PROMPT SENT TO GPT-5-NANO:")
            print("-"*50)
            print(self.system_prompt)
            print("-"*50)
            print(f"{'='*100}\n")
            
            # Invoke the agent with just the user input
            # The agent will use tools to get what it needs
            result = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            print(f"\n{'='*100}")
            print(f"!!! LLM RESPONSE - WHAT GPT-5-NANO DECIDED TO DO !!!")
            
            # Log what the LLM decided
            for msg in result.get("messages", []):
                msg_type = getattr(msg, 'type', 'unknown')
                if msg_type == 'ai' and hasattr(msg, 'tool_calls') and msg.tool_calls:
                    print(f"LLM DECIDED TO CALL TOOLS:")
                    for tool_call in msg.tool_calls:
                        print(f"  - Tool: {tool_call.get('name', 'unknown')}")
                        print(f"    Args: {tool_call.get('args', {})}")
                elif msg_type == 'tool':
                    print(f"TOOL RESPONSE: {msg.content}")
                elif msg_type == 'ai':
                    print(f"LLM TEXT RESPONSE: {msg.content}")
            
            print(f"{'='*100}\n")
            
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