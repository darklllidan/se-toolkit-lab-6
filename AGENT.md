# Agent Documentation

This agent is a CLI script that connects to an LLM to answer questions. It implements an **Agentic Loop**, allowing it to use local tools before returning a final answer.

## Provider
The agent uses the **Qwen Code API** (model: `qwen3-coder-plus`) hosted on a remote virtual machine.

## Tools
The agent has access to the following tools:
- `list_files(path)`: Lists all files and directories in a given path.
- `read_file(path)`: Reads the content of a specific file.
*Security:* Both tools use `os.path.abspath` validation to prevent directory traversal attacks (e.g., reading outside the project root).

## Agentic Loop
1. The user's question and available tool schemas are sent to the LLM.
2. The LLM decides whether to call a tool or give a final answer.
3. If a tool is called, the script executes it locally and feeds the result back to the LLM.
4. This loops until the LLM provides a final text response, capped at 10 iterations.

## How to run
```bash
uv run agent.py "How do you resolve a merge conflict?"