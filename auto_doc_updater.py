import requests
import os
import json
import re

def read_java_files(folder_path):
    all_code = ""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found!")
        return all_code
        
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    all_code += f"\n// --- FILE: {file} ---\n{f.read()}\n"
            except Exception as e:
                print(f"Error reading {file}: {e}")
    return all_code

def generate_markdown_docs(code):
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Generate concise API documentation in Markdown format.

SECTIONS REQUIRED:
1. # DP API Documentation
2. ## Core Components (List Controller and Service)
3. ## Business Rules Applied (List out the rules currently active in the code)
4. ## Flow Summary

CRITICAL RULE:
Output ONLY valid Markdown. Do not include introductory text like "Here is the doc".

CODE TO ANALYZE:
{code}"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def generate_mermaid_diagram(code):
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Analyze this DP API code and generate a visual Mermaid.js sequenceDiagram.

CRITICAL RULES:
1. You MUST output ONLY a valid JSON array of strings. 
2. First element MUST be "sequenceDiagram". Second element MUST be "autonumber".
3. Use the ACTUAL class names from the code (e.g., GACRule, QOHRule, DoDOverrideRule). DO NOT use generic names like "Rule1" or "Rule2".
4. Group participants into colored columns using the Mermaid 'box' syntax instead of 'rect'.

COLOR THEMES FOR BOXES:
- box rgba(255, 204, 229, 0.5) "External" (For Client)
- box rgba(230, 245, 255, 0.5) "API Layer" (For Controllers)
- box rgba(200, 255, 200, 0.5) "Business Logic" (For Services)
- box rgba(229, 204, 255, 0.5) "Rules Engine" (For individual Rules)

EXAMPLE FORMAT:
[
    "sequenceDiagram",
    "autonumber",
    "box rgba(255, 204, 229, 0.5) Client Layer",
    "participant Client",
    "end",
    "box rgba(200, 255, 200, 0.5) Services",
    "participant SearchService",
    "end",
    "Client->>SearchService: POST /search",
    "SearchService-->>Client: Return Result"
]

CODE TO ANALYZE:
{code}"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error connecting to Ollama: {e}"

def update_markdown_file(content):
    os.makedirs("output", exist_ok=True)
    file_path = "output/api_documentation.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ SUCCESS: Markdown File updated at -> {file_path}")

def update_mermaid_file(result):
    os.makedirs("output", exist_ok=True)
    file_path = "output/diagram.html"
    
    clean_res = result
    
    # JSON Parsing Logic
    try:
        start = result.find('[')
        end = result.rfind(']') + 1
        if start != -1 and end > start:
            json_str = result[start:end]
            diagram_lines = json.loads(json_str)
            clean_res = "\n".join(diagram_lines)
        else:
            raise ValueError("No JSON Array brackets found")
    except Exception as e:
        print(f"⚠️ JSON Parse Fallback triggered: {e}")
        clean_res = result.replace("```json", "").replace("```mermaid", "").replace("```", "").strip()
        
    # 🚨 MASTER FIX: We run this Regex formatting UNCONDITIONALLY.
    # Even if JSON succeeds, if the AI stuffed everything into one string, this will break it apart perfectly!
    clean_res = clean_res.replace("```json", "").replace("```mermaid", "").replace("```", "").strip()
    clean_res = clean_res.replace(" participant ", "\nparticipant ")
    clean_res = clean_res.replace(" box ", "\nbox ")
    clean_res = clean_res.replace(" end ", "\nend ")
    clean_res = clean_res.replace(" autonumber", "\nautonumber\n")
    clean_res = re.sub(r'\s+([A-Za-z0-9_]+->>)', r'\n\1', clean_res)
    clean_res = re.sub(r'\s+([A-Za-z0-9_]+-->>)', r'\n\1', clean_res)
    
    clean_res = clean_res.replace("sequenceDiagram", "sequenceDiagram\n")
    
    # Clean up empty lines
    clean_res = "\n".join([line.strip() for line in clean_res.split("\n") if line.strip()])

    common_style = """
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #172b4d; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: #f4f5f7; }
        h1 { color: #0052cc; border-bottom: 2px solid #0052cc; padding-bottom: 10px; text-align: center; }
        .mermaid { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; overflow-x: auto; }
    </style>
    """

    content = f"""<!DOCTYPE html>
<html>
<head>
    {common_style}
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
    <h1>KodeLens - Auto Updated Flow Diagram</h1>
    <div class="mermaid">
{clean_res}
    </div>
    <script>
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

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ SUCCESS: Visual Diagram updated at -> {file_path}")

# --- MAIN EXECUTION ---
print("Scanning Spring Boot Project...")
folder = "sample_code"
java_code = read_java_files(folder)

if java_code.strip() == "":
    print("No Java code found. Add files to sample_code/ folder.")
else:
    print(f"Found Java code! Length: {len(java_code)} characters.\n")
    
    print("What do you want to Auto-Update?")
    print("1. Markdown Documentation (.md)")
    print("2. Visual Sequence Diagram (.html)")
    print("3. Update BOTH (Will take a little longer)")
    
    choice = input("Choice (1/2/3): ")
    
    if choice in ['1', '3']:
        print("\nUpdating Markdown Docs... (Ollama is thinking 🧠)")
        md_result = generate_markdown_docs(java_code)
        if "Error" in md_result:
            print(md_result)
        else:
            clean_md = md_result.replace("```markdown", "").replace("```", "").strip()
            update_markdown_file(clean_md)
            
    if choice in ['2', '3']:
        print("\nUpdating Visual Diagram... (Ollama is drawing 🎨)")
        mermaid_result = generate_mermaid_diagram(java_code)
        if "Error" in mermaid_result:
            print(mermaid_result)
        else:
            update_mermaid_file(mermaid_result)
            
    print("\nAll tasks completed! Check the 'output' folder.")