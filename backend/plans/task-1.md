# Task 1: LLM Agent Plan

**LLM Provider & Model:**
We will use the Qwen Code API (model: `qwen3-coder-plus`) running locally on the VM.

**Agent Structure:**

1. Read configuration (`LLM_API_KEY`, `LLM_API_BASE`, `LLM_MODEL`) strictly from environment variables.
2. Accept the user's question via command-line arguments.
3. Make a REST API call to the OpenAI-compatible `/v1/chat/completions` endpoint.
4. Output the result strictly as a JSON object containing `answer` and `tool_calls` keys.
