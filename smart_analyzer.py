import requests
import os

def read_java_file(file_path):
    try:
        # 'with' ensures file automatically close (like try-with-resources)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found - {file_path}")
        return None

def scan_folder(folder_path):
    java_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            java_files.append(os.path.join(folder_path, file))
    return java_files

def analyze_full_flow(all_code):
    # Prompt updated to stop AI from chatting and only output Markdown
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: These files are part of Dispensing Pharmacies API - 
a pharmacy routing microservice.

TASK: Generate complete API documentation in Markdown format.

FORMAT:
Output ONLY raw Markdown code.
Do NOT include any introductory phrases like "Here is the documentation" or conversational text.
Start directly with the # headers.

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

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        print("ERROR: Ollama not running! Start with: ollama serve")
        return None

def save_multiple_formats(content, base_name):
    """Saves the AI output into both .md and .html files"""
    # 1. Create Output folder (Java: new File("output").mkdirs())
    os.makedirs("output", exist_ok=True)
    
    md_file = f"output/{base_name}.md"
    html_file = f"output/{base_name}.html"

    # 2. Markdown save 
    try:
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Markdown saved successfully: {md_file}")
    except Exception as e:
        print(f"Error saving Markdown: {e}")

    # 3. HTML save (Basic wrapper)
    try:
        with open(html_file, "w", encoding="utf-8") as f:
            html_wrapper = f"<html>\n<body>\n<pre>\n{content}\n</pre>\n</body>\n</html>"
            f.write(html_wrapper)
        print(f"HTML saved successfully: {html_file}")
    except Exception as e:
        print(f"Error saving HTML: {e}")


# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
# In Java  public static void main(String[] args) 

folder = "sample_code"
files = scan_folder(folder)
print(f"Found {len(files)} Java files\n")

all_code = ""
for file_path in files:
    filename = os.path.basename(file_path)
    code = read_java_file(file_path)
    if code is None:
        continue
    all_code += f"\n// FILE: {filename}\n{code}\n"

if all_code.strip() == "":
    print("No Java code found to analyze!")
else:
    print("Analyzing full flow with qwen2.5-coder...\n")
    result = analyze_full_flow(all_code)

    if result is None:
        print("Analysis failed!")
    else:
        # Pass the result to our new multi-format saver
        save_multiple_formats(result, "api_documentation")
        print("\nCompleted successfully!")