import pytest
import tempfile
import os
import json
from datetime import datetime
from services.task_manager import TaskManager


@pytest.mark.unit
class TestTaskManager:
    """Unit tests for TaskManager service"""
    
    @pytest.fixture
    def temp_task_file(self):
        """Create a temporary tasks.json file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file = f.name
        
        yield temp_file
        
        # Cleanup
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    
    @pytest.fixture
    def task_manager(self, temp_task_file):
        """Create a TaskManager instance with temporary file"""
        return TaskManager(storage_path=temp_task_file)
    
    def test_init_empty_file(self, task_manager):
        """Test initialization with empty tasks file"""
        tasks = task_manager.get_tasks()
        assert tasks == []
    
    def test_add_task(self, task_manager):
        """Test adding a single task"""
        task_manager.add_task("Test task")
        tasks = task_manager.get_tasks()
        
        assert len(tasks) == 1
        assert tasks[0]['text'] == "Test task"
        assert tasks[0]['completed'] == False
        assert tasks[0]['priority'] == 'medium'
        assert tasks[0]['category'] is None
        assert 'id' in tasks[0]
        assert 'created_at' in tasks[0]
        assert 'modified_at' in tasks[0]
    
    def test_add_task_with_priority_and_category(self, task_manager):
        """Test adding a task with priority and category"""
        task_manager.add_task("High priority task", priority="high", category="business")
        tasks = task_manager.get_tasks()
        
        assert len(tasks) == 1
        assert tasks[0]['text'] == "High priority task"
        assert tasks[0]['priority'] == "high"
        assert tasks[0]['category'] == "business"
    
    def test_toggle_task(self, task_manager):
        """Test toggling task completion status"""
        task_manager.add_task("Test task")
        tasks = task_manager.get_tasks()
        task_id = tasks[0]['id']
        
        # Toggle to completed
        task_manager.toggle_task(task_id)
        tasks = task_manager.get_tasks()
        assert tasks[0]['completed'] == True
        
        # Toggle back to incomplete
        task_manager.toggle_task(task_id)
        tasks = task_manager.get_tasks()
        assert tasks[0]['completed'] == False
    
    def test_delete_task(self, task_manager):
        """Test deleting a task"""
        task_manager.add_task("Task to delete")
        tasks = task_manager.get_tasks()
        task_id = tasks[0]['id']
        
        task_manager.delete_task(task_id)
        tasks = task_manager.get_tasks()
        assert len(tasks) == 0
    
    def test_update_task(self, task_manager):
        """Test updating task text"""
        task_manager.add_task("Original text")
        tasks = task_manager.get_tasks()
        task_id = tasks[0]['id']
        
        task_manager.update_task(task_id, text="Updated text")
        tasks = task_manager.get_tasks()
        assert tasks[0]['text'] == "Updated text"
    
    def test_get_tasks_by_priority(self, task_manager):
        """Test filtering tasks by priority"""
        task_manager.add_task("High task", priority="high")
        task_manager.add_task("Medium task", priority="medium")
        task_manager.add_task("Low task", priority="low")
        
        high_tasks = task_manager.get_tasks_by_priority("high")
        assert len(high_tasks) == 1
        assert high_tasks[0]['text'] == "High task"
    
    def test_get_tasks_by_category(self, task_manager):
        """Test filtering tasks by category"""
        task_manager.add_task("Business task", category="business")
        task_manager.add_task("Personal task", category="personal")
        task_manager.add_task("No category task")
        
        business_tasks = task_manager.get_tasks_by_category("business")
        assert len(business_tasks) == 1
        assert business_tasks[0]['text'] == "Business task"
    
    def test_get_pending_tasks(self, task_manager):
        """Test getting pending (incomplete) tasks"""
        task_manager.add_task("Pending task 1")
        task_manager.add_task("Pending task 2")
        task_manager.add_task("Completed task")
        
        # Complete one task
        tasks = task_manager.get_tasks()
        task_manager.toggle_task(tasks[2]['id'])
        
        pending_tasks = task_manager.get_pending_tasks()
        assert len(pending_tasks) == 2
        assert all(not task['completed'] for task in pending_tasks)
    
    def test_get_completed_tasks(self, task_manager):
        """Test getting completed tasks"""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        
        # Complete one task
        tasks = task_manager.get_tasks()
        task_manager.toggle_task(tasks[0]['id'])
        
        completed_tasks = task_manager.get_completed_tasks()
        assert len(completed_tasks) == 1
        assert all(task['completed'] for task in completed_tasks)
    
    def test_get_stats(self, task_manager):
        """Test getting task statistics"""
        task_manager.add_task("High business task", priority="high", category="business")
        task_manager.add_task("Medium personal task", priority="medium", category="personal")
        task_manager.add_task("Low task", priority="low")
        
        # Complete one task
        tasks = task_manager.get_tasks()
        task_manager.toggle_task(tasks[0]['id'])
        
        stats = task_manager.get_stats()
        
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2
        assert stats['high_priority'] == 1
        assert stats['medium_priority'] == 1
        assert stats['low_priority'] == 1
        assert stats['business_tasks'] == 1
        assert stats['personal_tasks'] == 1
    
    def test_clear_all(self, task_manager):
        """Test clearing all tasks"""
        task_manager.add_task("Task 1")
        task_manager.add_task("Task 2")
        
        task_manager.clear_all()
        tasks = task_manager.get_tasks()
        assert len(tasks) == 0
    
    def test_nonexistent_task_operations(self, task_manager):
        """Test operations on non-existent tasks"""
        # Try to toggle non-existent task
        task_manager.toggle_task("nonexistent_id")
        
        # Try to delete non-existent task
        task_manager.delete_task("nonexistent_id")
        
        # Try to update non-existent task
        task_manager.update_task("nonexistent_id", text="new text")
        
        # Should not crash and tasks should remain empty
        tasks = task_manager.get_tasks()
        assert len(tasks) == 0 