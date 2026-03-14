import os
import sys
import json
import requests

def main():
    # 1. Читаем доступы (авточекер подкинет сюда свои)
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE")
    model = os.getenv("LLM_MODEL")

    if not all([api_key, api_base, model]):
        print(json.dumps({"error": "Missing LLM environment variables", "answer": "", "tool_calls": []}))
        sys.exit(1)

    # 2. Берем вопрос из аргументов (если нет - задаем дефолтный)
    question = sys.argv[1] if len(sys.argv) > 1 else "Hello!"

    # 3. Собираем запрос к Qwen
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": question}]
    }

    try:
        # Дергаем API
        response = requests.post(f"{api_base}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Вытаскиваем ответ
        answer = data["choices"][0]["message"]["content"]
        
        # 4. Формируем идеальный JSON для авточекера
        result = {
            "answer": answer,
            "tool_calls": []  # Пока пусто, инструменты добавим в следующих тасках
        }
        print(json.dumps(result))

    except Exception as e:
        # Если что-то упало, всё равно отдаем структуру, чтобы не сломать парсер
        print(json.dumps({"error": str(e), "answer": "API Error", "tool_calls": []}))

if __name__ == "__main__":
    main()