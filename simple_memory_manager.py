"""
Simple Memory Manager - NO API REQUIRED
Works without OpenAI API - stores memories in JSON file locally
Perfect for demonstration when API quota is exhausted
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime

class SimpleMemoryManager:
    """
    Simple memory manager that stores data in a JSON file.
    No API calls needed - perfect for demo/testing.
    """
    
    def __init__(self):
        """Initialize simple memory storage."""
        self.memory_file = "simple_memories.json"
        self.memories = self._load_memories()
    
    def _load_memories(self) -> Dict:
        """Load memories from JSON file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_memories(self):
        """Save memories to JSON file."""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memories, f, indent=2, ensure_ascii=False)
    
    def add_memory(self, user_id: str, message: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Add a new memory for a user.
        
        Args:
            user_id (str): Unique identifier for the user
            message (str): The memory content to store
            metadata (dict, optional): Additional metadata
            
        Returns:
            dict: Result of the operation
        """
        try:
            if user_id not in self.memories:
                self.memories[user_id] = []
            
            memory_entry = {
                "id": f"mem_{len(self.memories[user_id])}_{datetime.now().timestamp()}",
                "text": message,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            self.memories[user_id].append(memory_entry)
            self._save_memories()
            
            print(f"✓ Memory added for user {user_id}")
            return {"status": "success", "result": memory_entry}
        except Exception as e:
            print(f"✗ Error adding memory: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_memories(self, user_id: str, query: Optional[str] = None) -> List[Dict]:
        """
        Retrieve memories for a user.
        
        Args:
            user_id (str): Unique identifier for the user
            query (str, optional): Search query (simple text match)
            
        Returns:
            list: List of memory dictionaries
        """
        try:
            user_memories = self.memories.get(user_id, [])
            
            if query:
                # Simple text search
                query_lower = query.lower()
                filtered = [m for m in user_memories 
                           if query_lower in m['text'].lower()]
                print(f"✓ Retrieved {len(filtered)} matching memories for user {user_id}")
                return filtered
            
            print(f"✓ Retrieved {len(user_memories)} memories for user {user_id}")
            return user_memories
        except Exception as e:
            print(f"✗ Error retrieving memories: {str(e)}")
            return []
    
    def delete_all_memories(self, user_id: str) -> Dict:
        """
        Delete all memories for a user.
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            dict: Result of the operation
        """
        try:
            if user_id in self.memories:
                del self.memories[user_id]
                self._save_memories()
            print(f"✓ All memories deleted for user {user_id}")
            return {"status": "success"}
        except Exception as e:
            print(f"✗ Error deleting memories: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def format_memories_for_context(self, memories: List[Dict]) -> str:
        """
        Format memories for display.
        
        Args:
            memories (list): List of memory dictionaries
            
        Returns:
            str: Formatted string
        """
        if not memories:
            return "No previous memories found."
        
        context = "Previous memories about the user:\n"
        for i, memory in enumerate(memories, 1):
            text = memory.get('text', '')
            context += f"{i}. {text}\n"
        
        return context