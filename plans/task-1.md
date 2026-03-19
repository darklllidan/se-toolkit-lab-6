# Task 1 Plan

**LLM Provider & Model:**
I will use the Qwen Code API hosted on my virtual machine. 
The model is `qwen3-coder-plus` (as configured in `.env.agent.secret`).

**Agent Structure (`agent.py`):**
1. Read the user's question from `sys.argv[1]`.
2. Load environment variables (`LLM_API_KEY`, `LLM_API_BASE`, `LLM_MODEL`) using `dotenv`.
3. Use the `openai` Python package to make a synchronous API call to the LLM.
4. Construct the output JSON containing `answer` and an empty `tool_calls` array.
5. Print the final JSON to stdout and any debug info to stderr.