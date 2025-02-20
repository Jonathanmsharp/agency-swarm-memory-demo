from agency_swarm import Agent
from pathlib import Path

from .tools.AddMemoryTool import AddMemoryTool
from .tools.SearchMemoryTool import SearchMemoryTool
from .tools.DeleteMemoryTool import DeleteMemoryTool


class CustomerSupportAgent(Agent):
    def __init__(self):
        current_dir = Path(__file__).parent
        super().__init__(
            name="Customer Support",
            description="A customer support agent with memory capabilities for personalized assistance.",
            instructions=str(current_dir / "instructions.md"),
            tools=[
                AddMemoryTool,
                SearchMemoryTool,
                DeleteMemoryTool
            ],
            temperature=0.5,
            max_prompt_tokens=25000,
        )

if __name__ == "__main__":
    # Test the agent
    agent = CustomerSupportAgent()
    print(f"Agent {agent.name} initialized with {len(agent.tools)} tools")
