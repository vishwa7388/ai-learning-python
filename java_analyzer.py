import requests
import os

def read_java_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def analyze_with_ai(code, filename):
    prompt = f"""ROLE: You are a Senior Spring Boot architect.

CONTEXT: This file is part of a pharmacy routing microservice 
called Dispensing Pharmacies API.

TASK: Analyze this Java file and explain the business flow.

FORMAT:
- Purpose (1 line)
- Input
- Output  
- External API Calls (if any)
- Business Logic Steps (in order)
Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

FILE: {filename}
CODE:
{code}"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]

# --- MAIN ---
file_path = "sample_code/SearchService.java"
print(f"Reading: {file_path}")

code = read_java_file(file_path)
print("Sending to AI...\n")

result = analyze_with_ai(code, os.path.basename(file_path))
print(result)

# --- Analyze second file ---
file_path2 = "sample_code/DrugAdaptor.java"
print(f"\n\nReading: {file_path2}")

code2 = read_java_file(file_path2)
print("Sending to AI...\n")

result2 = analyze_with_ai(code2, os.path.basename(file_path2))
print(result2)