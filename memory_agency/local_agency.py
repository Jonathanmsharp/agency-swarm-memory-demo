from agency_swarm import Agency
from agents.customer_support import CustomerSupportAgent
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Ensure OpenAI API key is present (needed for the agent's responses)
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Set memory path if not already set
    if not os.getenv("LOCAL_MEMORY_PATH"):
        os.environ["LOCAL_MEMORY_PATH"] = "local_memory.json"

    # Initialize the customer support agent
    support_agent = CustomerSupportAgent()

    # Create the agency with a single agent
    agency = Agency(
        [support_agent],  # Single agent setup
        shared_instructions="A customer support agency with local memory storage.",
        temperature=0.7,
        max_prompt_tokens=25000
    )

    # Run the agency in demo mode
    agency.run_demo()

if __name__ == "__main__":
    main() 