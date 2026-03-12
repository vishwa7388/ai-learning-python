import requests
import os

def read_java_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def scan_folder(folder_path):
    java_files = []
    if not os.path.exists(folder_path):
        return []
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            java_files.append(os.path.join(folder_path, file))
    return java_files

def analyze_with_ai(all_code, output_format):
    # 🚨 GURU MANTRA: Example-Based Prompting (Few-Shot)
    if output_format == "mermaid":
        instr = """Generate ONLY a visual Mermaid.js sequenceDiagram. 
        DO NOT generate tables. DO NOT use markdown backticks. 
        CRITICAL RULE: You MUST use a newline (\n) after EVERY statement. Do NOT write it all on one line.
        
        EXAMPLE FORMAT:
        sequenceDiagram
            participant Client
            participant Controller
            participant Service
            Client->>Controller: POST /search
            Controller->>Service: process()
        """
    elif output_format == "html":
        instr = """Generate professional documentation in HTML. 
        Use <h2> for classes, <h3> for methods. 
        Create a beautiful <table> for parameters and return types. 
        Do NOT use Markdown. Focus on Business Flow."""
    else:
        instr = "Generate Markdown format using ## and tables."

    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Analyze this DP API code and generate {output_format.upper()} documentation.
INSTRUCTION: {instr}
CODE:
{all_code}"""

    try:
        # Timeout set to 300s (5 minutes) for heavy lifting
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300) 
        return response.json().get("response", "")
    except requests.exceptions.Timeout:
        return "ERROR: AI took too long (300s). Try with fewer files."
    except Exception as e:
        return f"ERROR: {e}"

def save_output(result, fmt):
    os.makedirs("output", exist_ok=True)
    
    # Safai: Remove Markdown Backticks
    clean_res = result.replace("```mermaid", "").replace("```html", "").replace("```", "").strip()
    
    # 🚨 Python Fallback: Agar AI ne galti se fir ek line me likh diya (Fixing spacing)
    if fmt == "mermaid":
        clean_res = clean_res.replace(" participant ", "\n    participant ")
        clean_res = clean_res.replace(" Client->", "\n    Client->")
        clean_res = clean_res.replace(" Controller->", "\n    Controller->")
        clean_res = clean_res.replace(" Service->", "\n    Service->")
        clean_res = clean_res.replace(" Adaptor->", "\n    Adaptor->")
        clean_res = clean_res.replace(" ExternalAPI->", "\n    ExternalAPI->")
        clean_res = clean_res.replace("->>", "->>") # Normalize arrows
        clean_res = clean_res.replace("-->>", "-->>")

    # Beautiful Confluence CSS
    common_style = """
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #172b4d; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: #f4f5f7; }
        h1 { color: #0052cc; border-bottom: 2px solid #0052cc; padding-bottom: 10px; text-align: center; }
        h2 { color: #0052cc; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #dfe1e6; padding: 12px; text-align: left; }
        th { background-color: #f4f5f7; color: #5e6c84; }
        .mermaid { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; overflow-x: auto; }
    </style>
    """

    if fmt == "html":
        filename = "output/report.html"
        content = f"<html><head>{common_style}</head><body><h1>KodeLens API Report</h1>\n{clean_res}\n</body></html>"
    elif fmt == "mermaid":
        filename = "output/diagram.html"
        # 🎨 Confluence-style Colors configuration + Cursor JSON Fix
        content = f"""<!DOCTYPE html>
<html>
<head>
    {common_style}
    <script src="[https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js](https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js)"></script>
</head>
<body>
    <h1>KodeLens - Confluence Flow Diagram</h1>
    <div class="mermaid">
{clean_res}
    </div>
    <script>
        // Double brackets {{ }} for Python f-string escape
        const config = JSON.parse(`{{
            "startOnLoad": true, 
            "securityLevel": "loose", 
            "theme": "base",
            "themeVariables": {{
                "primaryColor": "#e9f2fa",
                "primaryTextColor": "#172b4d",
                "primaryBorderColor": "#0052cc",
                "lineColor": "#6b778c",
                "secondaryColor": "#fffae6",
                "tertiaryColor": "#e3fcef"
            }}
        }}`);
        mermaid.initialize(config);
    </script>
</body>
</html>"""
    else:
        filename = "output/report.md"
        content = clean_res

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ File Saved: {filename}")
    if fmt == "mermaid":
        print(f"👉 Go ahead and open 'output/diagram.html' in your browser!")

# --- MAIN EXECUTION ---
folder = "sample_code"
files = scan_folder(folder)

if not files:
    print(f"No Java files found in '{folder}' folder.")
else:
    print(f"Found {len(files)} Java files.")
    
    all_code = ""
    for f in files:
        c = read_java_file(f)
        if c: all_code += f"\n// FILE: {os.path.basename(f)}\n{c}\n"

    print("\nSelect Output Format:")
    print("1. HTML Report (Detailed Tables)")
    print("2. Mermaid Diagram (Visual Flow)")
    print("3. Markdown File (Text)")
    c = input("Choice (1/2/3): ")
    
    mapping = {"1": "html", "2": "mermaid", "3": "markdown"}
    selected = mapping.get(c, "markdown")
    
    print(f"\nProcessing {selected.upper()}... (Ollama is thinking 🧠, give it a minute)")
    res = analyze_with_ai(all_code, selected)
    
    if "ERROR" in res:
        print(res)
    else:
        save_output(res, selected)
        print("\nDone! KodeLens has finished generating docs.")