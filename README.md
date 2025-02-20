# Agency Swarm Memory Demo

A minimalist implementation of a customer support agent with long-term memory using [mem0](https://github.com/mem0ai/mem0) and Agency Swarm framework. The project demonstrates two approaches to memory management: API-based using Mem0's cloud service and local storage simulation.

## Features

- Long-term memory for customer support conversations
- Per-user memory isolation
- Semantic search with Mem0 API for intelligent context retrieval
- Automatic fallback to local storage with keyword-based search
- Conversation workflow with memory-enhanced responses
- Modular tool-based architecture for memory operations
- View stored memories in Mem0 dashboard at https://app.mem0.ai/dashboard/memories

## Example Conversation
```
User: I'd like to request a refund for my order 12345.
... (start a new conversation)
User: "I'd like to get a refund for my order 12345."
Agent: *searches memory for prior messages about order number*
Agent: "According to my information, you've already requested a refund for this order."
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
   python memory_agency/agency.py
   ```

### Local Storage Only
Run without mem0 API key to use local storage:
```bash
python memory_agency/agency.py
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
│   └── CustomerSupportAgent/
│       ├── CustomerSupportAgent.py  # Customer support agent implementation
│       ├── instructions.md          # Agent instructions
│       └── tools/
│           ├── AddMemory.py         # Store conversation messages
│           ├── SearchMemory.py      # Search past conversations
│           └── DeleteMemory.py      # Delete user memory
├── config.py                        # Configuration and memory client setup
├── agency.py
```

## Memory Operations

Both implementations provide three core operations through Agency Swarm tools:
- **Add Memory**: Store new conversation messages
- **Search Memory**: Retrieve relevant past conversations
- **Delete Memory**: Clear user-specific memory

## Testing

Test individual tools:
```bash
python memory_agency/agents/customer_support/tools/AddMemory.py
python memory_agency/agents/customer_support/tools/SearchMemory.py
python memory_agency/agents/customer_support/tools/DeleteMemory.py
```

## License

MIT
