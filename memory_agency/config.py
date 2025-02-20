import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path configuration
DATA_DIR = Path(__file__).parent.parent / "data"
MEMORY_PATH = str(DATA_DIR / "memory.json")

# API configuration
MEM0_API_KEY = os.getenv("MEM0_API_KEY")

def get_memory_client():
    """Get mem0 client if available and configured."""
    if MEM0_API_KEY:
        try:
            from mem0 import MemoryClient
            return MemoryClient()
        except ImportError:
            return None
    return None

def init_memory_store():
    """Initialize memory store file if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'w') as f:
            f.write("{}") 