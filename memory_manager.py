"""
Memory Manager Module using Mem0
This module handles memory storage and retrieval for the chatbot using the mem0 library.

Citation: 
- Mem0 Documentation: https://docs.mem0.ai/
- Mem0 GitHub: https://github.com/mem0ai/mem0
"""

import os
from mem0 import Memory
from typing import List, Dict, Optional
import json

class MemoryManager:
    """
    Manages student memories using the mem0 library.
    Handles storage, retrieval, and updates of user preferences and conversation history.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Memory Manager with mem0 configuration.
        Uses LOCAL storage only - no Mem0 API key required!
        
        Args:
            api_key (str, optional): OpenAI API key for embeddings. 
                                    If None, will try to read from environment.
        """
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required for mem0")
        
        # Set the API key as environment variable for mem0 to use
        os.environ['OPENAI_API_KEY'] = self.api_key
        
        # Configure mem0 with LOCAL storage (no Mem0 API key needed)
        # Updated configuration for newer mem0 versions
        config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
                    "temperature": 0.2,
                    "max_tokens": 1500,
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small",
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "student_memories",
                    "path": "./qdrant_data"  # Local storage - no cloud needed
                }
            }
        }
        
        # Initialize Memory instance with local configuration
        self.memory = Memory.from_config(config)
        
    def add_memory(self, user_id: str, message: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Add a new memory for a user.
        
        Args:
            user_id (str): Unique identifier for the user
            message (str): The memory content to store
            metadata (dict, optional): Additional metadata for the memory
            
        Returns:
            dict: Result of the memory addition operation
        """
        try:
            result = self.memory.add(
                messages=[{"role": "user", "content": message}],
                user_id=user_id,
                metadata=metadata or {}
            )
            print(f"✓ Memory added for user {user_id}: {message[:50]}...")
            return {"status": "success", "result": result}
        except Exception as e:
            print(f"✗ Error adding memory: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_memories(self, user_id: str, query: Optional[str] = None) -> List[Dict]:
        """
        Retrieve memories for a user, optionally filtered by a query.
        
        Args:
            user_id (str): Unique identifier for the user
            query (str, optional): Search query to filter relevant memories
            
        Returns:
            list: List of memory dictionaries
        """
        try:
            if query:
                # Search for relevant memories based on query
                memories = self.memory.search(query=query, user_id=user_id)
            else:
                # Get all memories for the user
                memories = self.memory.get_all(user_id=user_id)
            
            print(f"✓ Retrieved {len(memories)} memories for user {user_id}")
            return memories
        except Exception as e:
            print(f"✗ Error retrieving memories: {str(e)}")
            return []
    
    def update_memory(self, memory_id: str, data: str) -> Dict:
        """
        Update an existing memory.
        
        Args:
            memory_id (str): ID of the memory to update
            data (str): New content for the memory
            
        Returns:
            dict: Result of the update operation
        """
        try:
            result = self.memory.update(memory_id=memory_id, data=data)
            print(f"✓ Memory {memory_id} updated successfully")
            return {"status": "success", "result": result}
        except Exception as e:
            print(f"✗ Error updating memory: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def delete_memory(self, memory_id: str) -> Dict:
        """
        Delete a specific memory.
        
        Args:
            memory_id (str): ID of the memory to delete
            
        Returns:
            dict: Result of the deletion operation
        """
        try:
            self.memory.delete(memory_id=memory_id)
            print(f"✓ Memory {memory_id} deleted successfully")
            return {"status": "success"}
        except Exception as e:
            print(f"✗ Error deleting memory: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def delete_all_memories(self, user_id: str) -> Dict:
        """
        Delete all memories for a specific user.
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            dict: Result of the deletion operation
        """
        try:
            self.memory.delete_all(user_id=user_id)
            print(f"✓ All memories deleted for user {user_id}")
            return {"status": "success"}
        except Exception as e:
            print(f"✗ Error deleting all memories: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def format_memories_for_context(self, memories: List[Dict]) -> str:
        """
        Format retrieved memories into a context string for the chatbot.
        
        Args:
            memories (list): List of memory dictionaries
            
        Returns:
            str: Formatted string of memories for chatbot context
        """
        if not memories:
            return "No previous memories found."
        
        context = "Previous memories about the user:\n"
        for i, memory in enumerate(memories, 1):
            # Extract memory content based on mem0 response structure
            if isinstance(memory, dict):
                content = memory.get('memory', memory.get('text', str(memory)))
                context += f"{i}. {content}\n"
        
        return context