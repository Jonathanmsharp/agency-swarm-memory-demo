from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import List, Dict
import json
from memory_agency.config import MEMORY_PATH, get_memory_client, init_memory_store

class AddMemoryTool(BaseTool):
    """Store conversation messages into long-term memory."""
    messages: List[Dict[str, str]] = Field(
        ...,
        description="List of messages to store. Each message should be a dict with 'role' and 'content' keys."
    )
    user_id: str = Field(
        ...,
        description="Unique identifier for the user whose memory this belongs to."
    )

    def run(self) -> str:
        """Store the messages in memory and return a confirmation."""
        client = get_memory_client()
        if client:
            try:
                client.add(messages=self.messages, user_id=self.user_id, output_format="v1.1")
                return f"Successfully stored {len(self.messages)} messages for user {self.user_id}"
            except Exception as e:
                print(f"Warning: Failed to use mem0 API: {str(e)}")

        # Local storage fallback
        init_memory_store()
        try:
            with open(MEMORY_PATH, 'r') as f:
                memory_store = json.load(f)

            if self.user_id not in memory_store:
                memory_store[self.user_id] = []
            
            for msg in self.messages:
                memory_store[self.user_id].append({
                    "text": msg["content"],
                    "role": msg["role"]
                })
            
            with open(MEMORY_PATH, 'w') as f:
                json.dump(memory_store, f, indent=2)

            return f"Successfully stored {len(self.messages)} messages locally for user {self.user_id}"
        except Exception as e:
            return f"Error: Could not store messages: {str(e)}"


if __name__ == "__main__":
    tool = AddMemoryTool(
        messages=[
            {"role": "user", "content": "My order number is 12345"},
            {"role": "assistant", "content": "I've noted your order number: 12345"}
        ],
        user_id="test_user_1"
    )
    print(tool.run()) 