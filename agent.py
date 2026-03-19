import sys
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    # Проверяем, передали ли вопрос
    if len(sys.argv) < 2:
        print("Error: No question provided.", file=sys.stderr)
        sys.exit(1)
        
    question = sys.argv[1]
    
    # Грузим переменные из .env.agent.secret
    load_dotenv(".env.agent.secret")
    
    api_key = os.getenv("LLM_API_KEY")
    api_base = os.getenv("LLM_API_BASE")
    model = os.getenv("LLM_MODEL")

    if not all([api_key, api_base, model]):
        print("Error: Missing LLM configuration in .env.agent.secret", file=sys.stderr)
        sys.exit(1)

    # Инициализируем клиента OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )

    try:
        # Отправляем запрос (дебаг выводим в stderr)
        print(f"Sending question to {model}...", file=sys.stderr)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant."},
                {"role": "user", "content": question}
            ],
            timeout=60 # Ограничение в 60 секунд по условию
        )
        
        answer_text = response.choices[0].message.content

        # Формируем итоговый JSON
        output = {
            "answer": answer_text,
            "tool_calls": []
        }
        
        # Выводим ТОЛЬКО валидный JSON в stdout
        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        print(f"Error calling LLM: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()