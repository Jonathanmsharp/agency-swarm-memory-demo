from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from memory_agency.config import MEMORY_PATH, get_memory_client, init_memory_store


class DeleteMemoryTool(BaseTool):
    """Delete all stored memory for a specific user."""
    user_id: str = Field(
        ...,
        description="Unique identifier for the user whose memory to delete."
    )

    def run(self) -> str:
        """Delete all memories for the specified user."""
        client = get_memory_client()
        if client:
            try:
                client.delete_all(user_id=self.user_id)
                return f"Successfully deleted all memories for user {self.user_id}"
            except Exception as e:
                print(f"Warning: Failed to use mem0 API: {str(e)}")

        # Local storage fallback
        init_memory_store()
        try:
            with open(MEMORY_PATH, 'r') as f:
                memory_store = json.load(f)

            if self.user_id in memory_store:
                del memory_store[self.user_id]
                with open(MEMORY_PATH, 'w') as f:
                    json.dump(memory_store, f, indent=2)
                return f"Successfully deleted all memories for user {self.user_id}"
            return f"No memories found for user {self.user_id}"

        except Exception as e:
            return f"Error deleting memories: {str(e)}"


if __name__ == "__main__":
    tool = DeleteMemoryTool(user_id="test_user_1")
    print(tool.run()) 