# Agent Documentation

## Overview

This is a simple CLI-based LLM agent designed to answer user queries using the Qwen Code API.

## Configuration

The agent does not hardcode any credentials. It strictly relies on the following environment variables:

* `LLM_API_KEY`: Authentication token for the API.
* `LLM_API_BASE`: The base URL of the LLM provider (e.g., `http://<vm-ip>:<port>/v1`).
* `LLM_MODEL`: The model name (e.g., `qwen3-coder-plus`).

## How to Run

Run the agent via Python, passing your question as a string argument:

```bash
python agent.py "What is 2+2?"
```

## Output Format

The agent returns a JSON string to `stdout` containing the response and any requested tool operations:

```json
{
  "answer": "2 + 2 is 4.",
  "tool_calls": []
}
```
