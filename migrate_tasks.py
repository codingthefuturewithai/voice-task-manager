#!/usr/bin/env python3
"""
Migration script to convert existing tasks.json to the new enhanced format.
This script adds priority, category, and modified_at fields to existing tasks.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def migrate_tasks(tasks_file: str = "tasks.json"):
    """
    Migrate existing tasks to the new format
    """
    tasks_path = Path(tasks_file)
    
    if not tasks_path.exists():
        print(f"Tasks file {tasks_file} not found. Nothing to migrate.")
        return
    
    try:
        # Load existing tasks
        with open(tasks_path, 'r') as f:
            tasks = json.load(f)
        
        if not tasks:
            print("No tasks found. Nothing to migrate.")
            return
        
        print(f"Found {len(tasks)} tasks to migrate...")
        
        # Migrate each task
        migrated_count = 0
        for task in tasks:
            migrated = False
            
            # Add priority if missing
            if 'priority' not in task:
                task['priority'] = 'medium'  # Default priority
                migrated = True
            
            # Add category if missing
            if 'category' not in task:
                task['category'] = None  # Default category
                migrated = True
            
            # Add modified_at if missing
            if 'modified_at' not in task:
                task['modified_at'] = task['created_at']  # Use creation time as initial modification
                migrated = True
            
            if migrated:
                migrated_count += 1
        
        # Save migrated tasks
        with open(tasks_path, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        print(f"Successfully migrated {migrated_count} tasks!")
        print(f"Tasks saved to {tasks_path}")
        
        # Show sample of migrated task
        if tasks:
            print("\nSample migrated task:")
            sample_task = tasks[0]
            print(json.dumps(sample_task, indent=2))
        
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

def backup_tasks(tasks_file: str = "tasks.json"):
    """
    Create a backup of the tasks file before migration
    """
    tasks_path = Path(tasks_file)
    if tasks_path.exists():
        backup_path = tasks_path.with_suffix('.json.backup')
        import shutil
        shutil.copy2(tasks_path, backup_path)
        print(f"Backup created: {backup_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate tasks to enhanced format")
    parser.add_argument("--file", default="tasks.json", help="Tasks file to migrate")
    parser.add_argument("--backup", action="store_true", help="Create backup before migration")
    
    args = parser.parse_args()
    
    if args.backup:
        backup_tasks(args.file)
    
    migrate_tasks(args.file) 