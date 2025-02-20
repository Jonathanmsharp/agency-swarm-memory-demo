# Agency Swarm Memory Demo

A minimalist implementation of a customer support agent with long-term memory using [mem0](https://github.com/mem0ai/mem0) and Agency Swarm framework. The project demonstrates two approaches to memory management: API-based using Mem0's cloud service and local storage simulation.

## Features

- Long-term memory for customer support conversations
- Per-user memory isolation
- Semantic search with Mem0 API for intelligent context retrieval
- Automatic fallback to local storage with keyword-based search
- Conversation workflow with memory-enhanced responses
- Modular tool-based architecture for memory operations

## Example Conversation

```
User: "I can't remember my order number, but I asked about it earlier."
Agent: *searches memory for prior messages about order number*
Agent: "No problem, I have your order number as 12345 from our earlier chat."
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```

## Usage

### With mem0 API
1. Add your mem0 API key to `.env`:
   ```
   MEM0_API_KEY=your_api_key_here
   ```
2. Run the agency:
   ```bash
   python memory_agency/remote_agency.py
   ```

### Local Storage Only
Run without mem0 API key to use local storage:
```bash
python memory_agency/local_agency.py
```

## Implementation Approaches

### API-Based (Mem0 Cloud)
- Uses Mem0's managed cloud service for memory storage
- Semantic vector search for intelligent context retrieval
- Enterprise-grade security and automatic scaling
- Requires internet connectivity and API key

### Local Storage
- Fully self-contained implementation
- Simple keyword-based search (can be extended with local embeddings)
- Complete data privacy and control
- No external dependencies

## Project Structure

```
memory_agency/
├── agents/
│   └── customer_support/
│       ├── agent.py          # Customer support agent implementation
│       ├── instructions.md   # Agent instructions
│       └── tools/
│           ├── add_memory.py     # Store conversation messages
│           ├── search_memory.py  # Search past conversations
│           └── delete_memory.py  # Delete user memory
├── config.py         # Configuration and memory client setup
├── local_agency.py   # Local storage version
└── remote_agency.py  # mem0 API version
```

## Memory Operations

Both implementations provide three core operations through Agency Swarm tools:
- **Add Memory**: Store new conversation messages
- **Search Memory**: Retrieve relevant past conversations
- **Delete Memory**: Clear user-specific memory

## Testing

Test individual tools:
```bash
python memory_agency/agents/customer_support/tools/add_memory.py
python memory_agency/agents/customer_support/tools/search_memory.py
python memory_agency/agents/customer_support/tools/delete_memory.py
```

## License

MIT