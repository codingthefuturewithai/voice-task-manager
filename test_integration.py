#!/usr/bin/env python3
"""
Comprehensive integration tests for Voice Task Manager
Tests all services and data flow without UI or voice input
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.task_manager import TaskManager
from services.llm_service import LLMService
from services.command_router import CommandRouter
from services.task_matcher import TaskMatcher
from services.tts_service import TTSService

load_dotenv()

class TestVoiceTaskManager:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.tasks_file = os.path.join(self.temp_dir, "test_tasks.json")
        
        # Initialize services
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  No OpenAI API key found. Some tests will be skipped.")
            self.llm = None
        else:
            self.llm = LLMService(api_key)
        
        self.task_manager = TaskManager(self.tasks_file)
        self.command_router = CommandRouter(self.llm, self.task_manager) if self.llm else None
        self.task_matcher = TaskMatcher()
        self.tts = TTSService()
    
    def cleanup(self):
        """Clean up test files"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_task_manager_basic_operations(self):
        """Test basic task manager operations"""
        print("🧪 Testing TaskManager basic operations...")
        
        # Test adding tasks
        task1_id = self.task_manager.add_task("Test task 1", "high", "client")
        task2_id = self.task_manager.add_task("Test task 2", "medium", "business")
        task3_id = self.task_manager.add_task("Test task 3", "low", "personal")
        
        tasks = self.task_manager.get_tasks()
        assert len(tasks) == 3, f"Expected 3 tasks, got {len(tasks)}"
        
        # Test filtering
        high_tasks = self.task_manager.get_tasks_by_priority("high")
        assert len(high_tasks) == 1, f"Expected 1 high priority task, got {len(high_tasks)}"
        
        client_tasks = self.task_manager.get_tasks_by_category("client")
        assert len(client_tasks) == 1, f"Expected 1 client task, got {len(client_tasks)}"
        
        # Test updating tasks
        success = self.task_manager.update_task(task1_id, text="Updated task 1", priority="low")
        assert success, "Task update should succeed"
        
        updated_task = next(t for t in tasks if t['id'] == task1_id)
        assert updated_task['text'] == "Updated task 1", "Task text should be updated"
        assert updated_task['priority'] == "low", "Task priority should be updated"
        
        # Test toggling completion
        self.task_manager.toggle_task(task2_id)
        task2 = next(t for t in self.task_manager.get_tasks() if t['id'] == task2_id)
        assert task2['completed'], "Task should be marked as completed"
        
        # Test deleting tasks
        self.task_manager.delete_task(task3_id)
        remaining_tasks = self.task_manager.get_tasks()
        assert len(remaining_tasks) == 2, f"Expected 2 tasks after deletion, got {len(remaining_tasks)}"
        
        # Test statistics
        stats = self.task_manager.get_stats()
        assert stats['total'] == 2, f"Expected 2 total tasks, got {stats['total']}"
        assert stats['completed'] == 1, f"Expected 1 completed task, got {stats['completed']}"
        assert stats['high_priority'] == 0, f"Expected 0 high priority tasks, got {stats['high_priority']}"
        assert stats['low_priority'] == 1, f"Expected 1 low priority task, got {stats['low_priority']}"
        
        print("✅ TaskManager basic operations passed!")
    
    def test_task_matcher(self):
        """Test task matching functionality"""
        print("🧪 Testing TaskMatcher...")
        
        # Create test tasks
        test_tasks = [
            {"id": "1", "text": "Review quarterly report", "priority": "high", "category": "business"},
            {"id": "2", "text": "Call client about project", "priority": "medium", "category": "client"},
            {"id": "3", "text": "Fix login bug", "priority": "high", "category": "business"},
            {"id": "4", "text": "Schedule team meeting", "priority": "low", "category": "personal"}
        ]
        
        # Test exact match
        match = self.task_matcher.find_best_match("review quarterly report", test_tasks)
        assert match is not None, "Should find exact match"
        assert match['id'] == "1", f"Expected task 1, got {match['id']}"
        
        # Test partial match
        match = self.task_matcher.find_best_match("quarterly", test_tasks)
        assert match is not None, "Should find partial match"
        assert match['id'] == "1", f"Expected task 1, got {match['id']}"
        
        # Test no match
        match = self.task_matcher.find_best_match("completely unrelated task", test_tasks)
        assert match is None, "Should not find match for unrelated text"
        
        # Test multiple matches
        matches = self.task_matcher.find_multiple_matches("bug", test_tasks)
        assert len(matches) >= 1, f"Should find at least 1 task with 'bug', got {len(matches)}"
        
        print("✅ TaskMatcher tests passed!")
    
    def test_command_processing(self):
        """Test command processing without voice input"""
        print("🧪 Testing Command Processing...")
        
        if not self.llm:
            print("⚠️  Skipping command processing tests (no API key)")
            return
        
        # Add some test tasks
        self.task_manager.add_task("Review documentation", "medium", "business")
        self.task_manager.add_task("Fix login bug", "high", "business")
        
        current_tasks = self.task_manager.get_tasks()
        
        # Test query command
        result = self.command_router.process_command("What should I work on next?", "command", current_tasks)
        assert 'message' in result, "Result should contain message"
        assert result['intent'] in ['query', 'braindump'], f"Expected query intent, got {result['intent']}"
        
        # Test add command
        result = self.command_router.process_command("Add a task to test the system", "command", current_tasks)
        assert result['intent'] == 'add', f"Expected add intent, got {result['intent']}"
        
        print("✅ Command processing tests passed!")
    
    def test_data_persistence(self):
        """Test that data persists correctly"""
        print("🧪 Testing Data Persistence...")
        
        # Clear any existing tasks first
        self.task_manager.clear_all()
        
        # Add tasks
        self.task_manager.add_task("Persistent task 1", "high", "client")
        self.task_manager.add_task("Persistent task 2", "medium", "business")
        
        # Create new task manager instance (simulates app restart)
        new_task_manager = TaskManager(self.tasks_file)
        tasks = new_task_manager.get_tasks()
        
        assert len(tasks) == 2, f"Expected 2 tasks after restart, got {len(tasks)}"
        
        # Verify task structure
        for task in tasks:
            assert 'priority' in task, "Task should have priority field"
            assert 'category' in task, "Task should have category field"
            assert 'modified_at' in task, "Task should have modified_at field"
        
        print("✅ Data persistence tests passed!")
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("🧪 Testing Edge Cases...")
        
        # Create fresh task manager for this test
        edge_case_task_manager = TaskManager(self.tasks_file)
        edge_case_task_manager.clear_all()
        
        # Test empty task list
        empty_tasks = edge_case_task_manager.get_tasks()
        assert len(empty_tasks) == 0, "Should start with empty task list"
        
        # Test deleting non-existent task
        edge_case_task_manager.delete_task("non-existent-id")
        tasks = edge_case_task_manager.get_tasks()
        assert len(tasks) == 0, "Deleting non-existent task should not affect list"
        
        # Test updating non-existent task
        success = edge_case_task_manager.update_task("non-existent-id", text="test")
        assert not success, "Updating non-existent task should return False"
        
        # Test task matching with empty list
        match = self.task_matcher.find_best_match("test", [])
        assert match is None, "Should return None for empty task list"
        
        print("✅ Edge case tests passed!")
    
    def test_priority_category_defaults(self):
        """Test that tasks get proper default priority and category"""
        print("🧪 Testing Priority/Category Defaults...")
        
        # Create fresh task manager for this test
        defaults_task_manager = TaskManager(self.tasks_file)
        defaults_task_manager.clear_all()
        
        # Test adding task without specifying priority/category
        task_id = defaults_task_manager.add_task("Test default task")
        task = next(t for t in defaults_task_manager.get_tasks() if t['id'] == task_id)
        
        assert task['priority'] == 'medium', f"Expected medium priority, got {task['priority']}"
        assert task['category'] is None, f"Expected None category, got {task['category']}"
        
        # Test adding task with explicit defaults
        task_id2 = defaults_task_manager.add_task("Test explicit task", "medium", None)
        task2 = next(t for t in defaults_task_manager.get_tasks() if t['id'] == task_id2)
        
        assert task2['priority'] == 'medium', f"Expected medium priority, got {task2['priority']}"
        assert task2['category'] is None, f"Expected None category, got {task2['category']}"
        
        print("✅ Priority/category defaults tests passed!")
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Running Voice Task Manager Integration Tests\n")
        
        try:
            self.test_task_manager_basic_operations()
            self.test_task_matcher()
            self.test_command_processing()
            self.test_data_persistence()
            self.test_edge_cases()
            self.test_priority_category_defaults()
            
            print("\n🎉 All integration tests passed!")
            return True
            
        except Exception as e:
            print(f"\n❌ Integration test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            self.cleanup()

if __name__ == "__main__":
    tester = TestVoiceTaskManager()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1) 