import requests
import os

def read_java_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def analyze_with_ai(code, filename):
    prompt = f"""ROLE: You are a Senior Spring Boot architect.

CONTEXT: This file is part of a pharmacy routing microservice.

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

def scan_folder(folder_path):
    java_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            java_files.append(os.path.join(folder_path, file))
    return java_files

# --- MAIN ---
folder = "sample_code"
files = scan_folder(folder)
print(f"Found {len(files)} Java files\n")

for file_path in files:
    print(f"{'='*50}")
    print(f"Analyzing: {os.path.basename(file_path)}")
    print(f"{'='*50}")
    code = read_java_file(file_path)
    result = analyze_with_ai(code, os.path.basename(file_path))
    print(result)
    print()