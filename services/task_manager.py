import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

class TaskManager:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = Path(storage_path)
        self.tasks = self._load_tasks()
        # Migrate existing tasks if needed
        self._migrate_tasks()
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON file"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def _migrate_tasks(self):
        """Migrate old task format to new format"""
        migrated = False
        for task in self.tasks:
            if 'priority' not in task:
                task['priority'] = 'medium'  # Default priority
                migrated = True
            if 'category' not in task:
                task['category'] = None  # Default category
                migrated = True
            if 'modified_at' not in task:
                task['modified_at'] = task['created_at']  # Use creation time as initial modification
                migrated = True
        
        if migrated:
            self._save_tasks()
    
    def add_task(self, text: str, priority: str = 'medium', category: Optional[str] = None) -> str:
        """Add a new task with enhanced attributes"""
        now = datetime.now().isoformat()
        task = {
            'id': str(uuid.uuid4()),
            'text': text,
            'priority': priority,
            'category': category,
            'completed': False,
            'created_at': now,
            'modified_at': now,
            'completed_at': None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task['id']
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update task attributes"""
        for task in self.tasks:
            if task['id'] == task_id:
                # Update provided fields
                for key, value in kwargs.items():
                    if key in ['text', 'priority', 'category', 'completed']:
                        task[key] = value
                
                # Update modification timestamp
                task['modified_at'] = datetime.now().isoformat()
                
                # Handle completion timestamp
                if 'completed' in kwargs:
                    if kwargs['completed']:
                        task['completed_at'] = datetime.now().isoformat()
                    else:
                        task['completed_at'] = None
                
                self._save_tasks()
                return True
        return False
    
    def toggle_task(self, task_id: str):
        """Toggle task completion status"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['completed_at'] = datetime.now().isoformat() if task['completed'] else None
                task['modified_at'] = datetime.now().isoformat()
                self._save_tasks()
                break
    
    def delete_task(self, task_id: str):
        """Delete a task"""
        print(f"TaskManager: Deleting task {task_id}")
        print(f"TaskManager: Before delete - {len(self.tasks)} tasks")
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        print(f"TaskManager: After delete - {len(self.tasks)} tasks")
        self._save_tasks()
    
    def clear_all(self):
        """Clear all tasks"""
        self.tasks = []
        self._save_tasks()
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        return self.tasks
    
    def get_tasks_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by priority"""
        return [t for t in self.tasks if t['priority'] == priority]
    
    def get_tasks_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get tasks filtered by category"""
        return [t for t in self.tasks if t['category'] == category]
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all incomplete tasks"""
        return [t for t in self.tasks if not t['completed']]
    
    def get_completed_tasks(self) -> List[Dict[str, Any]]:
        """Get all completed tasks"""
        return [t for t in self.tasks if t['completed']]
    
    def get_stats(self) -> Dict[str, int]:
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        pending = total - completed
        
        # Priority breakdown
        high_priority = len(self.get_tasks_by_priority('high'))
        medium_priority = len(self.get_tasks_by_priority('medium'))
        low_priority = len(self.get_tasks_by_priority('low'))
        
        # Category breakdown
        client_tasks = len(self.get_tasks_by_category('client'))
        business_tasks = len(self.get_tasks_by_category('business'))
        personal_tasks = len(self.get_tasks_by_category('personal'))
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'client_tasks': client_tasks,
            'business_tasks': business_tasks,
            'personal_tasks': personal_tasks
        }