import requests
import os

def read_java_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def scan_folder(folder_path):
    java_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            java_files.append(os.path.join(folder_path, file))
    return java_files

def analyze_full_flow(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect.

CONTEXT: These files are part of Dispensing Pharmacies API - 
a pharmacy routing microservice.

TASK: Trace the COMPLETE request flow from entry point to final response.
Show how classes connect to each other.

FORMAT:
Step 1: [What happens] (which class, which method)
Step 2: [What happens] (which class, which method)
...continue until response is sent back.

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]

# --- MAIN ---
folder = "sample_code"
files = scan_folder(folder)
print(f"Found {len(files)} Java files\n")

all_code = ""
for file_path in files:
    filename = os.path.basename(file_path)
    code = read_java_file(file_path)
    all_code += f"\n// FILE: {filename}\n{code}\n"

print("Analyzing full flow...\n")
result = analyze_full_flow(all_code)
print(result)