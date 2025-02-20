from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import List, Dict
import json
from memory_agency.config import MEMORY_PATH, get_memory_client, init_memory_store


class SearchMemoryTool(BaseTool):
    """Search for relevant memories based on a query."""
    query: str = Field(
        ...,
        description="The search query to find relevant memories."
    )
    user_id: str = Field(
        ...,
        description="Unique identifier for the user whose memory to search."
    )
    top_k: int = Field(
        default=5,
        description="Maximum number of memories to return."
    )

    def run(self) -> List[Dict[str, str]]:
        """Search memory and return relevant messages."""
        client = get_memory_client()
        if client:
            try:
                return client.search(
                    query=self.query,
                    user_id=self.user_id,
                    output_format="v1.1",
                    top_k=self.top_k
                )
            except Exception as e:
                print(f"Warning: Failed to use mem0 API: {str(e)}")

        # Local storage fallback
        init_memory_store()
        try:
            with open(MEMORY_PATH, 'r') as f:
                memory_store = json.load(f)

            entries = memory_store.get(self.user_id, [])
            if not entries:
                return []

            query_terms = self.query.lower().split()
            matches = []
            for message in entries:
                text = message['text'].lower()
                if any(term in text for term in query_terms):
                    matches.append({
                        "text": message["text"],
                        "role": message["role"],
                        "score": 1.0 if all(term in text for term in query_terms) else 0.5
                    })

            matches.sort(key=lambda x: x["score"], reverse=True)
            return matches[:self.top_k]
        except Exception as e:
            print(f"Error searching memory: {str(e)}")
            return []


if __name__ == "__main__":
    tool = SearchMemoryTool(
        query="order number",
        user_id="test_user_1",
        top_k=3
    )
    results = tool.run()
    print("Found memories:", results)
