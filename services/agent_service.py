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
            List all tasks in the system with their IDs.
            
            IMPORTANT: This returns task IDs that you need for other operations like toggle_task.
            
            Args:
                show_completed: Whether to include completed tasks (default: False, only shows pending)
            
            Returns:
                A formatted list of tasks with their IDs, status, text, and priority
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
            for i, task in enumerate(task_list, 1):
                status = "✅" if task.get('completed', False) else "⬜"
                priority = task.get('priority', 'medium') or 'medium'  # Handle None
                category = task.get('category', 'none') or 'none'  # Handle None
                result += f"{i}. {status} [{task['id']}] {task['text']} (Priority: {priority}, Category: {category})\n"
            
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
        def complete_task(task_id: str) -> str:
            """
            Mark a task as complete or incomplete by toggling its status.
            
            IMPORTANT: You must first call list_tasks to get the task IDs, then use the exact ID here.
            
            Args:
                task_id: The UUID of the task (e.g., '5e1986b6-7e1f-445f-8ea0-b0be817ba232')
                        This is the 'id' field shown in brackets when you list tasks.
            
            Returns:
                Success message confirming the action
                
            Example workflow:
                1. User says "mark buy milk as complete"
                2. Call list_tasks() to see all tasks with their IDs
                3. Find the task with text "buy milk" and note its ID in brackets
                4. Call complete_task with that ID
            """
            print(f"\n{'='*50}")
            print(f"COMPLETE_TASK TOOL CALLED BY LLM")
            print(f"task_id: {task_id}")
            print(f"{'='*50}\n")
            
            # Get task info before toggle for better message
            tasks = task_manager.get_tasks()
            task = next((t for t in tasks if t['id'] == task_id), None)
            
            if not task:
                return f"❌ Error: No task found with ID '{task_id}'"
            
            # Toggle the task
            task_manager.toggle_task(task_id)
            
            # Get updated status
            was_completed = task.get('completed', False)
            new_status = "completed ✅" if not was_completed else "incomplete ⬜"
            
            print(f"TASK TOGGLED: '{task['text']}' is now {new_status}")
            return f"Task '{task['text']}' is now {new_status}"
        
        @tool
        def update_task(task_id: str, text: Optional[str] = None, priority: Optional[str] = None, category: Optional[str] = None) -> str:
            """
            Update an existing task's properties.
            
            You can update the text, priority, category, or any combination of these.
            First call list_tasks to get the task ID you want to update.
            
            Args:
                task_id: The UUID of the task to update (from list_tasks output)
                text: New text/description for the task (optional)
                priority: New priority level - must be 'high', 'medium', or 'low' (optional)
                category: New category - must be 'client', 'business', or 'personal' (optional)
            
            Returns:
                Success message confirming what was updated
                
            Examples:
                - "Change priority of task X to high" → update_task(id, priority="high")
                - "Move task Y to client category" → update_task(id, category="client")
                - "Rename task Z to 'Review contracts'" → update_task(id, text="Review contracts")
            """
            print(f"\n{'='*50}")
            print(f"UPDATE_TASK TOOL CALLED BY LLM")
            print(f"task_id: {task_id}")
            print(f"text: {text}")
            print(f"priority: {priority}")
            print(f"category: {category}")
            print(f"{'='*50}\n")
            
            # Build kwargs for update
            kwargs = {}
            if text is not None:
                kwargs['text'] = text
            if priority is not None:
                if priority not in ['high', 'medium', 'low']:
                    return f"❌ Error: Priority must be 'high', 'medium', or 'low', not '{priority}'"
                kwargs['priority'] = priority
            if category is not None:
                if category not in ['client', 'business', 'personal']:
                    return f"❌ Error: Category must be 'client', 'business', or 'personal', not '{category}'"
                kwargs['category'] = category
            
            if not kwargs:
                return "❌ Error: No updates specified. Provide at least one field to update."
            
            # Get task info for better message
            tasks = task_manager.get_tasks()
            task = next((t for t in tasks if t['id'] == task_id), None)
            
            if not task:
                return f"❌ Error: No task found with ID '{task_id}'"
            
            success = task_manager.update_task(task_id, **kwargs)
            
            if success:
                updates = []
                if text: updates.append(f"text to '{text}'")
                if priority: updates.append(f"priority to '{priority}'")
                if category: updates.append(f"category to '{category}'")
                print(f"TASK UPDATED: '{task['text']}' - {', '.join(updates)}")
                return f"✅ Updated '{task['text']}': {', '.join(updates)}"
            else:
                return f"❌ Error: Failed to update task '{task['text']}'"
        
        @tool
        def delete_task(task_id: str) -> str:
            """
            Permanently delete a task from the system.
            
            WARNING: This action cannot be undone. The task will be permanently removed.
            First call list_tasks to get the task ID you want to delete.
            
            Args:
                task_id: The UUID of the task to delete (from list_tasks output)
            
            Returns:
                Success message confirming deletion
                
            Example:
                User: "Delete the task about reviewing contracts"
                1. Call list_tasks() to find the task
                2. Call delete_task with the task's ID
            """
            print(f"\n{'='*50}")
            print(f"DELETE_TASK TOOL CALLED BY LLM")
            print(f"task_id: {task_id}")
            print(f"{'='*50}\n")
            
            # Get task info before deletion for confirmation message
            tasks = task_manager.get_tasks()
            task = next((t for t in tasks if t['id'] == task_id), None)
            
            if not task:
                return f"❌ Error: No task found with ID '{task_id}'"
            
            task_text = task['text']
            task_manager.delete_task(task_id)
            
            print(f"TASK DELETED: '{task_text}'")
            return f"✅ Task deleted: '{task_text}'"
        
        @tool
        def get_tasks_by_priority(priority: str) -> str:
            """
            Get all tasks filtered by a specific priority level.
            
            Args:
                priority: Priority level to filter by - must be 'high', 'medium', or 'low'
            
            Returns:
                Formatted list of tasks with the specified priority
                
            Examples:
                - "Show me all high priority tasks" → get_tasks_by_priority("high")
                - "What are my low priority items?" → get_tasks_by_priority("low")
            """
            print(f"\n{'='*50}")
            print(f"GET_TASKS_BY_PRIORITY TOOL CALLED BY LLM")
            print(f"priority: {priority}")
            print(f"{'='*50}\n")
            
            if priority not in ['high', 'medium', 'low']:
                return f"❌ Error: Priority must be 'high', 'medium', or 'low', not '{priority}'"
            
            tasks = task_manager.get_tasks_by_priority(priority)
            
            if not tasks:
                return f"No {priority} priority tasks found."
            
            result = f"{priority.capitalize()} Priority Tasks:\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get('completed', False) else "⬜"
                category = task.get('category', 'none')
                result += f"{i}. {status} [{task['id']}] {task['text']} (Category: {category})\n"
            
            print(f"FOUND {len(tasks)} {priority} priority tasks")
            return result
        
        @tool
        def get_tasks_by_category(category: str) -> str:
            """
            Get all tasks filtered by a specific category.
            
            Args:
                category: Category to filter by - must be 'client', 'business', or 'personal'
            
            Returns:
                Formatted list of tasks in the specified category
                
            Examples:
                - "Show me all client tasks" → get_tasks_by_category("client")
                - "What business tasks do I have?" → get_tasks_by_category("business")
                - "List my personal items" → get_tasks_by_category("personal")
            """
            print(f"\n{'='*50}")
            print(f"GET_TASKS_BY_CATEGORY TOOL CALLED BY LLM")
            print(f"category: {category}")
            print(f"{'='*50}\n")
            
            if category not in ['client', 'business', 'personal']:
                return f"❌ Error: Category must be 'client', 'business', or 'personal', not '{category}'"
            
            tasks = task_manager.get_tasks_by_category(category)
            
            if not tasks:
                return f"No {category} tasks found."
            
            result = f"{category.capitalize()} Tasks:\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get('completed', False) else "⬜"
                priority = task.get('priority', 'medium')
                result += f"{i}. {status} [{task['id']}] {task['text']} (Priority: {priority})\n"
            
            print(f"FOUND {len(tasks)} {category} tasks")
            return result
        
        @tool
        def get_pending_tasks() -> str:
            """
            Get all incomplete/pending tasks that still need to be done.
            
            This is useful for seeing what work remains without the clutter of completed items.
            
            Returns:
                Formatted list of all incomplete tasks with their IDs, priorities, and categories
                
            Example:
                - "What do I still need to do?" → get_pending_tasks()
                - "Show me incomplete tasks" → get_pending_tasks()
            """
            print(f"\n{'='*50}")
            print(f"GET_PENDING_TASKS TOOL CALLED BY LLM")
            print(f"{'='*50}\n")
            
            tasks = task_manager.get_pending_tasks()
            
            if not tasks:
                return "🎉 No pending tasks! Everything is complete."
            
            result = "Pending Tasks:\n"
            for i, task in enumerate(tasks, 1):
                priority = task.get('priority', 'medium')
                category = task.get('category', 'none')
                result += f"{i}. ⬜ [{task['id']}] {task['text']} (Priority: {priority}, Category: {category})\n"
            
            print(f"FOUND {len(tasks)} pending tasks")
            return result
        
        @tool
        def get_completed_tasks() -> str:
            """
            Get all completed tasks.
            
            This shows tasks that have been marked as done, useful for reviewing accomplishments.
            
            Returns:
                Formatted list of all completed tasks with their completion status
                
            Example:
                - "What have I completed?" → get_completed_tasks()
                - "Show me finished tasks" → get_completed_tasks()
            """
            print(f"\n{'='*50}")
            print(f"GET_COMPLETED_TASKS TOOL CALLED BY LLM")
            print(f"{'='*50}\n")
            
            tasks = task_manager.get_completed_tasks()
            
            if not tasks:
                return "No completed tasks yet."
            
            result = "Completed Tasks:\n"
            for i, task in enumerate(tasks, 1):
                priority = task.get('priority', 'medium')
                category = task.get('category', 'none')
                result += f"{i}. ✅ [{task['id']}] {task['text']} (Priority: {priority}, Category: {category})\n"
            
            print(f"FOUND {len(tasks)} completed tasks")
            return result
        
        @tool
        def get_task_stats() -> str:
            """
            Get comprehensive statistics about all tasks.
            
            Provides a summary including total tasks, completion status, priority breakdown,
            and category distribution. Useful for getting a high-level overview.
            
            Returns:
                Formatted statistics summary with counts and percentages
                
            Example:
                - "Show me task statistics" → get_task_stats()
                - "How many tasks do I have?" → get_task_stats()
                - "Give me a task summary" → get_task_stats()
            """
            print(f"\n{'='*50}")
            print(f"GET_TASK_STATS TOOL CALLED BY LLM")
            print(f"{'='*50}\n")
            
            stats = task_manager.get_stats()
            
            # Calculate completion percentage
            completion_pct = 0
            if stats['total'] > 0:
                completion_pct = (stats['completed'] / stats['total']) * 100
            
            result = "📊 Task Statistics:\n"
            result += f"\nOverall:\n"
            result += f"  • Total tasks: {stats['total']}\n"
            result += f"  • Completed: {stats['completed']} ({completion_pct:.1f}%)\n"
            result += f"  • Pending: {stats['pending']}\n"
            
            result += f"\nBy Priority:\n"
            result += f"  • High: {stats['high_priority']}\n"
            result += f"  • Medium: {stats['medium_priority']}\n"
            result += f"  • Low: {stats['low_priority']}\n"
            
            result += f"\nBy Category:\n"
            result += f"  • Client: {stats['client_tasks']}\n"
            result += f"  • Business: {stats['business_tasks']}\n"
            result += f"  • Personal: {stats['personal_tasks']}\n"
            
            print(f"STATS RETURNED: {stats['total']} total, {stats['completed']} completed")
            return result
        
        # Return list of tools - now includes all task management capabilities
        return [
            list_tasks, 
            add_task, 
            complete_task,
            update_task,
            delete_task,
            get_tasks_by_priority,
            get_tasks_by_category,
            get_pending_tasks,
            get_completed_tasks,
            get_task_stats
        ]
    
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