#!/usr/bin/env python3
"""
Test script for the enhanced Voice Task Manager functionality.
This script tests the new features without requiring voice input.
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.task_manager import TaskManager
from services.llm_service import LLMService
from services.command_router import CommandRouter
from services.task_matcher import TaskMatcher

load_dotenv()

def test_task_manager():
    """Test the enhanced TaskManager functionality"""
    print("🧪 Testing TaskManager...")
    
    # Create a temporary task manager
    task_manager = TaskManager("test_tasks.json")
    
    # Test adding tasks with different priorities and categories
    task_manager.add_task("Test high priority task", "high", "client")
    task_manager.add_task("Test medium priority task", "medium", "business")
    task_manager.add_task("Test low priority task", "low", "personal")
    task_manager.add_task("Test task without category", "medium")
    
    # Verify tasks were added
    tasks = task_manager.get_tasks()
    assert len(tasks) == 4, f"Expected 4 tasks, got {len(tasks)}"
    
    # Test filtering
    high_tasks = task_manager.get_tasks_by_priority("high")
    assert len(high_tasks) == 1, f"Expected 1 high priority task, got {len(high_tasks)}"
    
    client_tasks = task_manager.get_tasks_by_category("client")
    assert len(client_tasks) == 1, f"Expected 1 client task, got {len(client_tasks)}"
    
    # Test updating tasks
    first_task = tasks[0]
    success = task_manager.update_task(first_task['id'], text="Updated task text", priority="low")
    assert success, "Task update should succeed"
    
    # Test statistics
    stats = task_manager.get_stats()
    assert 'high_priority' in stats, "Stats should include priority breakdown"
    assert 'client_tasks' in stats, "Stats should include category breakdown"
    
    # Clean up
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
    
    print("✅ TaskManager tests passed!")

def test_task_matcher():
    """Test the TaskMatcher functionality"""
    print("🧪 Testing TaskMatcher...")
    
    # Create test tasks
    test_tasks = [
        {"id": "1", "text": "Review quarterly report", "priority": "high", "category": "business"},
        {"id": "2", "text": "Call client about project", "priority": "medium", "category": "client"},
        {"id": "3", "text": "Fix login bug", "priority": "high", "category": "business"},
        {"id": "4", "text": "Schedule team meeting", "priority": "low", "category": "personal"}
    ]
    
    # Test finding best match
    matcher = TaskMatcher()
    
    # Test exact match
    match = matcher.find_best_match("review quarterly report", test_tasks)
    assert match is not None, "Should find exact match"
    assert match['id'] == "1", f"Expected task 1, got {match['id']}"
    
    # Test partial match
    match = matcher.find_best_match("quarterly", test_tasks)
    assert match is not None, "Should find partial match"
    assert match['id'] == "1", f"Expected task 1, got {match['id']}"
    
    # Test no match
    match = matcher.find_best_match("completely unrelated task", test_tasks)
    assert match is None, "Should not find match for unrelated text"
    
    # Test multiple matches - look for tasks that contain "high" in their text or have high priority
    matches = matcher.find_multiple_matches("bug", test_tasks)
    assert len(matches) >= 1, f"Should find at least 1 task with 'bug', got {len(matches)}"
    
    print("✅ TaskMatcher tests passed!")

def test_command_processing():
    """Test command processing functionality"""
    print("🧪 Testing Command Processing...")
    
    # Skip if no API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Skipping command processing tests (no API key)")
        return
    
    # Create services
    task_manager = TaskManager("test_tasks.json")
    llm_service = LLMService(api_key)
    command_router = CommandRouter(llm_service, task_manager)
    
    # Add some test tasks
    task_manager.add_task("Review documentation", "medium", "business")
    task_manager.add_task("Fix login bug", "high", "business")
    
    # Test command processing
    current_tasks = task_manager.get_tasks()
    
    # Test a simple query
    result = command_router.process_command("What should I work on next?", "command", current_tasks)
    assert 'message' in result, "Result should contain message"
    assert result['intent'] in ['query', 'braindump'], f"Expected query intent, got {result['intent']}"
    
    print("✅ Command processing tests passed!")
    
    # Clean up
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")

def main():
    """Run all tests"""
    print("🚀 Running Voice Task Manager Enhancement Tests\n")
    
    try:
        test_task_manager()
        test_task_matcher()
        test_command_processing()
        
        print("\n🎉 All tests passed! The enhanced Voice Task Manager is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 