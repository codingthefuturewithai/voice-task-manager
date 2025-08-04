from difflib import SequenceMatcher
from typing import List, Dict, Any, Optional
import re

class TaskMatcher:
    @staticmethod
    def find_best_match(query: str, tasks: List[Dict[str, Any]], threshold: float = 0.6) -> Optional[Dict[str, Any]]:
        """
        Find task that best matches natural language description
        Uses fuzzy string matching and keyword extraction
        """
        if not tasks or not query:
            return None
        
        best_match = None
        best_score = 0
        
        # Clean and normalize query
        query_lower = query.lower().strip()
        
        for task in tasks:
            task_text = task['text'].lower()
            
            # Calculate similarity score
            score = SequenceMatcher(None, query_lower, task_text).ratio()
            
            # Boost score for keyword matches
            query_words = set(re.findall(r'\w+', query_lower))
            task_words = set(re.findall(r'\w+', task_text))
            
            # Calculate word overlap
            common_words = query_words.intersection(task_words)
            if common_words:
                word_overlap = len(common_words) / max(len(query_words), len(task_words))
                score = max(score, word_overlap * 0.8)  # Boost but don't override exact matches
            
            # Check for exact substring matches
            if query_lower in task_text or task_text in query_lower:
                score = max(score, 0.9)
            
            # Check for priority/category matches
            if 'high priority' in query_lower and task.get('priority') == 'high':
                score += 0.1
            elif 'low priority' in query_lower and task.get('priority') == 'low':
                score += 0.1
            elif 'client' in query_lower and task.get('category') == 'client':
                score += 0.1
            elif 'business' in query_lower and task.get('category') == 'business':
                score += 0.1
            elif 'personal' in query_lower and task.get('category') == 'personal':
                score += 0.1
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = task
        
        return best_match
    
    @staticmethod
    def find_multiple_matches(query: str, tasks: List[Dict[str, Any]], threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find multiple tasks that match the query
        Returns list of tasks sorted by match score
        """
        if not tasks or not query:
            return []
        
        matches = []
        query_lower = query.lower().strip()
        
        for task in tasks:
            task_text = task['text'].lower()
            score = SequenceMatcher(None, query_lower, task_text).ratio()
            
            # Apply same boosting logic as find_best_match
            query_words = set(re.findall(r'\w+', query_lower))
            task_words = set(re.findall(r'\w+', task_text))
            common_words = query_words.intersection(task_words)
            
            if common_words:
                word_overlap = len(common_words) / max(len(query_words), len(task_words))
                score = max(score, word_overlap * 0.8)
            
            if query_lower in task_text or task_text in query_lower:
                score = max(score, 0.9)
            
            if score >= threshold:
                matches.append((task, score))
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)
        return [task for task, score in matches]
    
    @staticmethod
    def extract_task_references(text: str, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract all task references from a piece of text
        Useful for commands that might reference multiple tasks
        """
        if not tasks or not text:
            return []
        
        referenced_tasks = []
        text_lower = text.lower()
        
        for task in tasks:
            task_text = task['text'].lower()
            
            # Check if task text appears in the command
            if task_text in text_lower:
                referenced_tasks.append(task)
            else:
                # Check for partial matches
                task_words = set(re.findall(r'\w+', task_text))
                text_words = set(re.findall(r'\w+', text_lower))
                common_words = task_words.intersection(text_words)
                
                # If more than 50% of task words are in the text, consider it referenced
                if len(common_words) / len(task_words) > 0.5:
                    referenced_tasks.append(task)
        
        return referenced_tasks 