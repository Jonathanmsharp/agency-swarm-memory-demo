import os

from agency_swarm import Agency
from agents.CustomerSupportAgent import CustomerSupportAgent
from dotenv import load_dotenv

load_dotenv()


def main(user_id: str):
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    support_agent = CustomerSupportAgent()

    agency = Agency(
        [support_agent],
        shared_instructions="A customer support agency with memory capabilities.",
        temperature=0.5,
        max_prompt_tokens=25000,
    )
    support_agent.shared_state.set("user_id", user_id)

    agency.run_demo()


if __name__ == "__main__":
    user_id = "user_123"
    main(user_id)
