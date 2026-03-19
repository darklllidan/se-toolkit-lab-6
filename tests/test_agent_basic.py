import subprocess
import json

def test_agent_basic_response():
    # Запускаем агента
    result = subprocess.run(
        ["uv", "run", "agent.py", "What is 2+2? Answer strictly with a single number."],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Пытаемся распарсить stdout как JSON
    try:
        output_data = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        assert False, f"Stdout is not valid JSON. Stdout: {result.stdout}"
        
    # Проверяем обязательные поля
    assert "answer" in output_data, "Missing 'answer' field"
    assert "tool_calls" in output_data, "Missing 'tool_calls' field"
    assert isinstance(output_data["tool_calls"], list), "'tool_calls' should be a list"
    assert len(output_data["tool_calls"]) == 0, "'tool_calls' should be empty for task 1"