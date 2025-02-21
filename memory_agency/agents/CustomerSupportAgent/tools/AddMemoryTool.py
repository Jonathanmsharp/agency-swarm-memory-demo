import os
from typing import Dict, List

from agency_swarm.tools import BaseTool
from mem0 import Memory, MemoryClient
from mem0.configs.base import MemoryConfig
from pydantic import Field


class AddMemoryTool(BaseTool):
    """Store conversation messages into long-term memory.

    Example:
        messages=[
            {"role": "user", "content": "My order number is 12345"},
            {"role": "assistant", "content": "I've noted your order number: 12345"}
        ]
    """

    messages: List[Dict[str, str]] = Field(
        ...,
        description="List of messages to store. Each message should be a dict with 'role' and 'content' keys.",
    )

    def run(self) -> str:
        """Store the messages in memory and return a confirmation."""
        if api_key := os.getenv("MEM0_API_KEY"):
            client = MemoryClient(api_key=api_key)
        else:
            client = None
        user_id = self._shared_state.get("user_id", "user_123")

        if client:
            try:
                response = client.add(
                    messages=self.messages, user_id=user_id, output_format="v1.1"
                )
                return f"Successfully stored {len(self.messages)} messages for user {user_id}. Response: {response}"
            except Exception as e:
                print(f"Warning: Failed to use mem0 API: {str(e)}")

        # Local storage fallback using Memory()
        local_memory = Memory(config=MemoryConfig(version="v1.1"))
        if not local_memory:
            return "Error: Could not initialize local memory storage"

        try:
            local_memory.add(messages=self.messages, user_id=user_id)
            return f"Successfully stored {len(self.messages)} messages locally for user {user_id}"
        except Exception as e:
            return f"Error: Could not store messages: {str(e)}"


if __name__ == "__main__":
    tool = AddMemoryTool(
        messages=[
            {"role": "user", "content": "My order number is 12345"},
            {"role": "assistant", "content": "I've noted your order number: 12345"},
        ]
    )
    print(tool.run())
