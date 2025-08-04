import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import uuid

class TaskManager:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = Path(storage_path)
        self.tasks = self._load_tasks()
    
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
    
    def add_task(self, text: str) -> str:
        """Add a new task"""
        task = {
            'id': str(uuid.uuid4()),
            'text': text,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task['id']
    
    def toggle_task(self, task_id: str):
        """Toggle task completion status"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['completed_at'] = datetime.now().isoformat() if task['completed'] else None
                self._save_tasks()
                break
    
    def delete_task(self, task_id: str):
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self._save_tasks()
    
    def clear_all(self):
        """Clear all tasks"""
        self.tasks = []
        self._save_tasks()
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        return self.tasks
    
    def get_stats(self) -> Dict[str, int]:
        """Get task statistics"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t['completed'])
        return {
            'total': total,
            'completed': completed,
            'pending': total - completed
        }