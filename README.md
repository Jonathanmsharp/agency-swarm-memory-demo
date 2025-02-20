# Agency Swarm Memory Demo

A minimalist implementation of a customer support agent with long-term memory using [mem0](https://github.com/mem0ai/mem0) and Agency Swarm framework.

## Features

- Long-term memory for customer support conversations
- Per-user memory isolation
- Automatic fallback to local storage when mem0 API is unavailable
- Simple keyword-based search for local storage

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

## Testing

Test individual tools:
```bash
python memory_agency/agents/customer_support/tools/add_memory.py
python memory_agency/agents/customer_support/tools/search_memory.py
python memory_agency/agents/customer_support/tools/delete_memory.py
```

## License

MIT