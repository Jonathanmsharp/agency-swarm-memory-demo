from agency_swarm import Agency
from agents.customer_support import CustomerSupportAgent
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    # Ensure required API keys are present
    if not os.getenv("MEM0_API_KEY"):
        raise ValueError("MEM0_API_KEY not found in environment variables")
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    # Initialize the customer support agent
    support_agent = CustomerSupportAgent()

    # Create the agency with a single agent
    agency = Agency(
        [support_agent],  # Single agent setup
        shared_instructions="A customer support agency with memory capabilities.",
        temperature=0.7,
        max_prompt_tokens=25000
    )

    # Run the agency in demo mode
    agency.run_demo()

if __name__ == "__main__":
    main() 