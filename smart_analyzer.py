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
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: These files are part of Dispensing Pharmacies API - 
a pharmacy routing microservice.

TASK: Generate complete API documentation.

FORMAT:
Generate output in clean HTML format.
Use <h2> for sections, <table> for tables, <ol> for steps.
Do NOT use Markdown. Use only HTML tags.

Sections:
1. Overview (What does this API do - 2 lines max)
2. Entry Point (Controller, endpoint, HTTP method)
3. Request (What fields come in the request)
4. Processing Flow (Step by step)
5. External API Calls (table: API Name, Purpose, Called From)
6. Business Rules (List each rule and what it does)
7. Response (What fields go back in response)

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

# --- SAVE TO HTML ---
output_file = "output/api_documentation.html"
os.makedirs("output", exist_ok=True)

with open(output_file, "w") as f:
    f.write("<html><body>\n")
    f.write("<h1>Dispensing Pharmacies API - Documentation</h1>\n")
    f.write(f"<p><strong>Files Analyzed:</strong> {len(files)}</p>\n")
    f.write("<hr>\n")
    f.write(result)
    f.write("\n</body></html>")

print(f"\nSaved to: {output_file}")