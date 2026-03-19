# Task 2 Plan: The Documentation Agent

**Tools:**
1. `list_files(path)`: Uses `os.listdir()` to return a list of files.
2. `read_file(path)`: Uses `open().read()` to return file contents.

**Security:**
To prevent directory traversal (e.g., `../../etc/passwd`), I will use `os.path.abspath()` to resolve the requested path and check if it `startswith()` the absolute path of the project root. If not, the tool will return an "Access denied" error.

**Agentic Loop:**
1. Send the user prompt + system prompt + tool schemas to the LLM.
2. Loop up to 10 times.
3. If `tool_calls` are present in the response, iterate over them, execute the corresponding local Python function securely, and append the result as a `tool` role message.
4. If no `tool_calls` are present, extract the `answer` and `source` from the LLM's final response, combine it with the `tool_calls` history, output the JSON to stdout, and exit.