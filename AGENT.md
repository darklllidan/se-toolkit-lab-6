# Agent Documentation

This agent is a simple CLI script that connects to an LLM to answer questions.

## Provider
The agent uses the **Qwen Code API** (model: `qwen3-coder-plus`) hosted on a remote virtual machine.

## How to run
1. Ensure `.env.agent.secret` is properly configured with your API key and base URL.
2. Run the agent using `uv`:

```bash
uv run agent.py "What is the capital of France?"
```