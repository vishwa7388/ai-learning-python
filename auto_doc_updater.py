import requests
import os
import json
import re

def read_java_files(folder_path):
    all_code = ""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' nahi mila!")
        return all_code
        
    for file in os.listdir(folder_path):
        if file.endswith(".java"):
            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    all_code += f"\n// --- FILE: {file} ---\n{f.read()}\n"
            except Exception as e:
                print(f"File padhne mein error {file}: {e}")
    return all_code

def generate_markdown_docs(code):
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Generate concise API documentation in Markdown format.
SECTIONS: Overview, Core Components, Business Rules (with logic), Flow Summary.
CODE:
{code}"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

def generate_mermaid_diagram(code):
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Generate a Mermaid.js sequenceDiagram JSON array.

CRITICAL RULES:
1. Output ONLY a valid JSON array of strings.
2. Participant definitions MUST be separate from interaction arrows.
3. Use 'box' syntax for layers. 
4. Participants inside the box should NOT have quotes in the name.
5. Flow interactions (arrows) must follow the participant definitions.

EXAMPLE:
["sequenceDiagram", "autonumber", "box rgba(230, 245, 255, 0.5) API", "participant SearchController", "end", "SearchController->>SearchService: process"]

CODE:
{code}"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

def generate_security_audit(code):
    prompt = f"""ROLE: Cyber Security Expert. Analyze for vulnerabilities. Code: {code}"""
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "qwen2.5-coder:7b",
            "prompt": prompt,
            "stream": False
        }, timeout=300)
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

def update_mermaid_file(result):
    os.makedirs("output", exist_ok=True)
    file_path = "output/diagram.html"
    
    # 1. Cleaning raw text
    raw_text = result.replace("```json", "").replace("```mermaid", "").replace("```", "").strip()
    clean_res = ""
    
    # 2. JSON Parsing
    try:
        start = raw_text.find('[')
        end = raw_text.rfind(']') + 1
        if start != -1 and end > start:
            json_str = raw_text[start:end]
            diagram_lines = json.loads(json_str)
            clean_res = "\n".join(diagram_lines)
        else:
            clean_res = raw_text
    except:
        clean_res = raw_text

    # 3. Aggressive Formatting Fix (The "Anti-Jhantupana" logic)
    # Ensure sequenceDiagram is the first line
    clean_res = re.sub(r'\bsequenceDiagram\b', 'sequenceDiagram\n', clean_res)
    
    # Force newlines for keywords
    keywords = ["autonumber", "participant", "box", "alt", "else", "end", "rect", "loop"]
    for kw in keywords:
        clean_res = re.sub(rf'(?<!\n)\s*\b({kw})\b', rf'\n\1', clean_res)
    
    # Force newlines for arrows (very important!)
    clean_res = re.sub(r'(?<!\n)\s*(\S+[-]{1,2}>>)', r'\n\1', clean_res)
    
    # Final cleanup of line noise
    lines = []
    for line in clean_res.split('\n'):
        l = line.strip().strip('"').strip("'").strip(',').strip()
        if l and l.lower() != "null":
            # If line contains both participant and arrow, split them
            if "participant" in l and "->" in l:
                sub_parts = re.split(r'(?=->|-->>)', l)
                for sp in sub_parts:
                    if sp.strip(): lines.append(sp.strip())
            else:
                lines.append(l)
    
    final_clean = "\n".join(lines)

    common_style = """
    <style>
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f4f5f7; padding: 40px; }
        h1 { color: #0052cc; text-align: center; border-bottom: 2px solid #0052cc; padding-bottom: 10px; margin-bottom: 30px; }
        .mermaid { 
            background: white; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 8px 24px rgba(0,0,0,0.12); 
            display: block; 
            margin: 0 auto;
            max-width: 95%;
            overflow-x: auto;
            white-space: pre;
        }
    </style>
    """

    # 🚨 FIXED CDN LINK: Pure HTML, no markdown brackets
    content = f"""<!DOCTYPE html>
<html>
<head>
    {common_style}
    <script src="[https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js](https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js)"></script>
</head>
<body>
    <h1>KodeLens - Professional Design Flow</h1>
    <div class="mermaid">
{final_clean}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            securityLevel: 'loose',
            themeVariables: {{
                primaryColor: '#e9f2fa',
                primaryTextColor: '#172b4d',
                primaryBorderColor: '#0052cc',
                lineColor: '#6b778c'
            }}
        }});
    </script>
</body>
</html>"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ SUCCESS: Visual Diagram rendered at -> {file_path}")

def update_markdown_file(content, filename):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w", encoding="utf-8") as f:
        f.write(content.replace("```markdown", "").replace("```", "").strip())
    print(f"✅ SUCCESS: {filename} updated.")

# --- MAIN ---
print("Scanning project...")
java_code = read_java_files("sample_code")
if java_code:
    print("1. Docs  2. Diagram  3. Audit  4. All")
    c = input("Choice: ")
    if c in ['1', '4']: update_markdown_file(generate_markdown_docs(java_code), "api_doc.md")
    if c in ['2', '4']: update_mermaid_file(generate_mermaid_diagram(java_code))
    if c in ['3', '4']: update_markdown_file(generate_security_audit(java_code), "security_audit.md")