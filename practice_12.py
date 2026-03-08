import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5-coder:7b",
        "prompt": "Explain what is Spring Boot in 2 lines",
        "stream": False
    }
)

data = response.json()
print(f"AI says:\\n{data['response']}")