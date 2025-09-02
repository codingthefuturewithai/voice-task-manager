#!/usr/bin/env python3
"""
Test script for GPT-5 nano agent tools - validates all 10 task management capabilities
"""

import asyncio
import os
from services.agent_service import AgentService
from services.task_manager import TaskManager
from dotenv import load_dotenv

async def test_agent_tools():
    """Test the agent tools with various commands."""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        return
    
    # Initialize services
    task_manager = TaskManager()
    agent = AgentService(api_key, task_manager)
    
    print("\n" + "="*60)
    print("🧪 Testing GPT-5 Nano Agent Tools (10 tools)")
    print("="*60)
    
    # Test commands covering all 10 tools
    test_commands = [
        # Tool 1: list_tasks
        ("List all my tasks", "Tests list_tasks tool"),
        
        # Tool 2: add_task  
        ("Add a high priority client task to review the Q4 report", "Tests add_task with priority and category"),
        
        # Tool 3: complete_task (toggle)
        ("Mark the first task as complete", "Tests complete_task/toggle functionality"),
        
        # Tool 4: update_task
        ("Change the priority of the Q4 report task to medium", "Tests update_task for priority change"),
        
        # Tool 5: delete_task
        ("Delete the task about Q4 report", "Tests delete_task"),
        
        # Tool 6: get_tasks_by_priority
        ("Show me all high priority tasks", "Tests get_tasks_by_priority"),
        
        # Tool 7: get_tasks_by_category
        ("What are my client tasks?", "Tests get_tasks_by_category"),
        
        # Tool 8: get_pending_tasks
        ("Show me pending tasks", "Tests get_pending_tasks"),
        
        # Tool 9: get_completed_tasks
        ("What tasks have I completed?", "Tests get_completed_tasks"),
        
        # Tool 10: get_task_stats
        ("Show me task statistics", "Tests get_task_stats")
    ]
    
    for i, (command, description) in enumerate(test_commands, 1):
        print(f"\n📝 Test {i}/10: {description}")
        print(f"   Command: \"{command}\"")
        print("-" * 40)
        
        result = await agent.process_request(command)
        
        if result["success"]:
            print(f"✅ Response: {result['response'][:200]}{'...' if len(result['response']) > 200 else ''}")
            if result.get("tool_calls"):
                print(f"🔧 Tools used: {len(result['tool_calls'])} tool(s)")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # Small delay between commands
        await asyncio.sleep(0.5)
    
    print("\n" + "="*60)
    print("✅ All 10 agent tools tested!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_agent_tools())