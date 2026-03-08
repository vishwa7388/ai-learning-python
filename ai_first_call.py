import requests

def ask_ai(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5-coder:7b",
            "prompt": question,
            "stream": False
        }
    )
    return response.json()['response']

# Ab AI se kuch bhi puch!
print(ask_ai("Explain what is REST API in 2 lines"))
print("\n---\n")
print(ask_ai("Write a simple Python function to add two numbers"))
print("\n---\n")
print(ask_ai("What is the difference between Java and Python in 3 points"))