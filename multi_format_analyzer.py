import requests
import os

def read_java_file(file_path):
    try:
        # UTF-8 encoding is good practice for Java files 
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

def analyze_with_ai(all_code, output_format):
    # Smart Prompting: Har format ke liye alag instruction 
    format_instructions = {
        "html": "Generate output in clean HTML. Use <h2> for sections, <table> for tables, <ol> for steps. Do NOT use Markdown.",
        "markdown": "Generate output in Markdown. Use ## for sections, | for tables, - for lists.",
        "text": "Generate output in plain text. Use simple formatting with dashes and numbers."
    }

    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice. [cite: 3]

TASK: Generate complete API documentation.

FORMAT:
{format_instructions[output_format]}

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
        # Connecting to local Ollama [cite: 3]
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        print("ERROR: Ollama not running! Start with: ollama serve")
        return None

def save_output(result, output_format, file_count):
    os.makedirs("output", exist_ok=True)
    
    extensions = {"html": "html", "markdown": "md", "text": "txt"}
    output_file = f"output/api_documentation.{extensions[output_format]}"
    
    with open(output_file, "w", encoding="utf-8") as f:
        if output_format == "html":
            # Proper HTML wrapper for browser viewing 
            f.write("<html><body style='font-family: Arial, sans-serif; padding: 20px;'>\n")
            f.write("<h1>Dispensing Pharmacies API - Documentation</h1>\n")
            f.write(f"<p><strong>Files Analyzed:</strong> {file_count}</p>\n")
            f.write("<hr>\n")
            f.write(result)
            f.write("\n</body></html>")
        elif output_format == "markdown":
            f.write("# Dispensing Pharmacies API - Documentation\n\n")
            f.write(f"**Files Analyzed:** {file_count}\n\n")
            f.write("---\n\n")
            f.write(result)
        else:
            f.write("Dispensing Pharmacies API - Documentation\n")
            f.write(f"Files Analyzed: {file_count}\n")
            f.write("=" * 50 + "\n\n")
            f.write(result)
    
    print(f"\n✅ Saved to: {output_file}")

# --- MAIN EXECUTION ---
folder = "sample_code"
files = scan_folder(folder)
print(f"Found {len(files)} Java files for KodeLens analysis.\n")

all_code = ""
for file_path in files:
    filename = os.path.basename(file_path)
    code = read_java_file(file_path)
    if code:
        all_code += f"\n// FILE: {filename}\n{code}\n"

if not all_code:
    print("No code found!")
else:
    # User choice (Like Java Scanner)
    print("Choose output format:")
    print("1. HTML (Confluence style)")
    print("2. Markdown (GitHub style)")
    print("3. Plain Text")
    choice = input("Enter choice (1/2/3): ")

    format_map = {"1": "html", "2": "markdown", "3": "text"}
    selected_format = format_map.get(choice, "markdown")

    print(f"\nAnalyzing in {selected_format.upper()} format... Please wait.\n")
    result = analyze_with_ai(all_code, selected_format)

    if result:
        print("-" * 30)
        print(result[:500] + "...") # Sirf preview dikhane ke liye
        save_output(result, selected_format, len(files))