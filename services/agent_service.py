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
            prompt="""You are a helpful Voice Task Manager assistant who can take actions directly in the system.

CRITICAL INSTRUCTIONS:
When you successfully use a tool to perform an action:
- The tool itself will return a success message like "✅ Successfully added task..."
- DO NOT add any additional explanation after the tool message
- DO NOT explain how the user could have done it themselves
- DO NOT provide manual instructions
- Just let the tool's success message be your entire response

When the user asks "how to" do something (without requesting the action):
- Explain the voice commands they can use
- Provide helpful instructions

Examples:
- User: "Add a task to buy milk" → Use tool, response is just the tool's success message
- User: "How do I add tasks?" → Explain voice commands (don't use tools)"""
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
            
            Args:
                text: The task description
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
        def complete_task(task_description: str) -> str:
            """
            Mark a task as completed/done in the user's task list.
            
            This tool should be called when the user wants to mark a task as finished.
            The tool will search for the task by matching the description and mark it complete.
            
            Common phrases that trigger this tool:
            - "Mark ... as done"
            - "Complete the task..."
            - "I finished..."
            - "Check off..."
            - "Task ... is done"
            - "I completed..."
            - "Mark ... complete"
            - "Done with..."
            - "Finished..."
            - "Cross off..."
            
            Args:
                task_description: A description that identifies which task to complete.
                                 This can be partial text that matches a task.
            
            Examples:
                User: "Mark buy groceries as done" -> complete_task("buy groceries")
                User: "I finished calling the dentist" -> complete_task("calling the dentist")
                User: "Complete the contract review task" -> complete_task("contract review")
                User: "Check off watering the plants" -> complete_task("watering the plants")
                User: "Done with the equity agreement" -> complete_task("equity agreement")
            
            Returns:
                Success message if task was found and marked complete,
                or an error message if no matching task was found.
            """
            try:
                # Get all tasks
                tasks = task_manager.get_tasks()
                
                # Find matching task (case-insensitive partial match)
                matching_task = None
                task_description_lower = task_description.lower()
                
                for task in tasks:
                    if not task.get('completed', False):  # Only look at incomplete tasks
                        task_text = task.get('text', '').lower()
                        if task_description_lower in task_text or task_text in task_description_lower:
                            matching_task = task
                            break
                
                if matching_task:
                    # Mark the task as complete
                    task_manager.toggle_task(matching_task['id'])
                    return f"✅ Marked as complete: '{matching_task['text']}'"
                else:
                    # No matching task found
                    pending_tasks = [t['text'] for t in tasks if not t.get('completed', False)]
                    if pending_tasks:
                        task_list = '\n'.join([f"- {t}" for t in pending_tasks[:5]])
                        return f"❌ Could not find a task matching '{task_description}'.\n\nYour pending tasks:\n{task_list}"
                    else:
                        return "❌ No pending tasks to complete."
                
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
            # Build the full prompt with context
            prompt = user_input
            if context and context.get("current_tasks"):
                task_count = len(context["current_tasks"])
                pending_tasks = [t for t in context["current_tasks"] if not t.get('completed', False)]
                pending_count = len(pending_tasks)
                prompt = f"""Context: The user has {task_count} total tasks ({pending_count} pending).

User request: {user_input}

Remember: If this is an action request (like "add a task"), use the appropriate tool and just confirm what you did. Don't explain how they could do it manually."""
            
            # Invoke the agent
            result = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": prompt}]
            })
            
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