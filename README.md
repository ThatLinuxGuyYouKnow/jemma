# Jemma v2: Your Free Code Assistant

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LiteLLM](https://img.shields.io/badge/litellm-multi%20model-brightgreen)](https://github.com/BerriAI/litellm)

**Description:** Jemma is a command-line code assistant powered by LLMs. v2 is a complete refactor with a modular architecture — agent loop, pluggable tools, and multi-model support via LiteLLM.

**Installation:**

```bash
pip install .
```

**Configuration:**

Before using Jemma, configure your API key:

```bash
jemma-init
```

Alternatively, set the `GEMINI_API_KEY` environment variable.

**Project Structure:**

```
jemma/
├── agent/              # Agent loop orchestration
│   └── loop.py
├── exceptions/         # Custom exceptions
│   ├── file_operation_exceptions.py
│   ├── inference_exceptions.py
│   └── tool_call_exceptions.py
├── services/           # Core services
│   └── tool_service.py
├── tools/              # Pluggable tool definitions
│   ├── file_operations/
│   │   ├── read_file.py
│   │   └── write_to_file.py
│   ├── search_tools/
│   │   └── grep_search.py
│   └── registry.py
├── validators/         # Input validation for tools
│   ├── file_operations_validators.py
│   └── tool_call_validators.py
├── agentic_response.py
├── inference.py
├── message_enum.py
└── response_enums.py
tests/
└── test_tools.py
```

**Tools:**

| Tool | Description |
|------|-------------|
| `read_file` | Read file content with optional line ranges |
| `write_to_file` | Edit existing files by replacing content |
| `write_new_file` | Create and write to new files |
| `grep_search` | Search for patterns across files and directories |

**What's New in v2:**

- Modular architecture with agent loop, tools, and validators
- Tool registry with schema definitions for LLM function calling
- Multi-model support via LiteLLM
- Streaming inference with recursive tool call execution
- Pluggable tool system — easy to add new tools
- Input validation layer for tool arguments and file operations
- TUI support via Textual

## Roadmap

- [x] Complete agent loop with tool call handling
- [x] Add support for more models via LiteLLM
- [x] Improve error handling and logging
- [x] Add unit tests
- [ ] Create command for starting new projects
- [ ] Add more tools (shell execution, web fetch)