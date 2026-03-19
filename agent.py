import sys
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

def is_safe_path(base_dir, target_path):
    """Предотвращает выход за пределы папки проекта (Directory Traversal)."""
    base = os.path.abspath(base_dir)
    target = os.path.abspath(os.path.join(base, target_path))
    return target.startswith(base)

def list_files(base_dir, path):
    if not is_safe_path(base_dir, path):
        return "Error: Access denied. Cannot access paths outside the project root."
    target = os.path.join(base_dir, path)
    if not os.path.isdir(target):
        return f"Error: Directory '{path}' not found."
    try:
        return "\n".join(os.listdir(target))
    except Exception as e:
        return str(e)

def read_file(base_dir, path):
    if not is_safe_path(base_dir, path):
        return "Error: Access denied. Cannot access paths outside the project root."
    target = os.path.join(base_dir, path)
    if not os.path.isfile(target):
        return f"Error: File '{path}' not found."
    try:
        with open(target, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

def main():
    if len(sys.argv) < 2:
        print("Error: No question provided.", file=sys.stderr)
        sys.exit(1)
        
    question = sys.argv[1]
    load_dotenv(".env.agent.secret")
    
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE")
    model = os.getenv("LLM_MODEL")

    if not all([api_key, api_base, model]):
        print("Error: Missing LLM configuration in .env.agent.secret", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=api_base)
    project_root = os.getcwd()

    # Определяем инструменты (Tools) для LLM
    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_files",
                "description": "List files and directories at a given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative directory path from project root"}
                    },
                    "required": ["path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from the project repository.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Relative path from project root"}
                    },
                    "required": ["path"]
                }
            }
        }
    ]

    system_prompt = (
        "You are a documentation agent. You can use tools to read the project wiki and find answers. "
        "Use `list_files` to discover wiki files, and `read_file` to read their contents. "
        "When you have found the answer, you must respond strictly with a valid JSON object containing exactly two keys: "
        "1. 'answer': your final detailed answer to the user.\n"
        "2. 'source': the wiki file path and section anchor (e.g., 'wiki/git-workflow.md#resolving-merge-conflicts').\n"
        "Do not include Markdown formatting (like ```json) in your final response, just the raw JSON object."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    tool_calls_history = []
    max_iterations = 10

    # AGENTIC LOOP
    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}: Calling LLM...", file=sys.stderr)
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            timeout=60
        )
        
        message = response.choices[0].message
        messages.append(message) # Сохраняем ответ LLM в историю сообщений

        # Если LLM решила использовать инструмент
        if message.tool_calls:
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"Executing tool: {func_name}({args})", file=sys.stderr)
                
                result_str = ""
                if func_name == "list_files":
                    result_str = list_files(project_root, args.get("path", ""))
                elif func_name == "read_file":
                    result_str = read_file(project_root, args.get("path", ""))
                else:
                    result_str = "Error: Unknown tool."

                # Передаем результат обратно в LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": result_str
                })
                
                # Записываем в итоговую историю
                tool_calls_history.append({
                    "tool": func_name,
                    "args": args,
                    "result": result_str[:1000] + ("..." if len(result_str) > 1000 else "") # Обрезаем слишком длинные выводы для чистоты JSON
                })
        else:
            # Если tool_calls нет — это финальный ответ
            print("Final answer received.", file=sys.stderr)
            try:
                final_data = json.loads(message.content)
                output = {
                    "answer": final_data.get("answer", message.content),
                    "source": final_data.get("source", "Unknown"),
                    "tool_calls": tool_calls_history
                }
            except Exception:
                output = {
                    "answer": message.content,
                    "source": "Unknown",
                    "tool_calls": tool_calls_history
                }
            print(json.dumps(output))
            sys.exit(0)
    
    # Если за 10 шагов не нашли ответ
    print("Error: Reached maximum tool calls (10).", file=sys.stderr)
    output = {
        "answer": "Error: Reached maximum tool calls.",
        "source": "None",
        "tool_calls": tool_calls_history
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()