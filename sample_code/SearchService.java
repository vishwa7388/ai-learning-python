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
    # Generalized prompt to handle ANY business logic automatically
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Generate concise API documentation in Markdown format.

SECTIONS REQUIRED:
1. # DP API Documentation
2. ## Core Components (List Controller and Service)
3. ## Business Rules Applied (Identify and explain all business rules and conditional logic found in the code)
4. ## Flow Summary

CRITICAL RULE:
Output ONLY valid Markdown. Do not include introductory text.

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
        return f"Ollama se connect karne mein error: {e}"

def generate_mermaid_diagram(code):
    # Generalized prompt to handle ANY sequence flow automatically
    prompt = f"""ROLE: Senior Spring Boot Architect.
TASK: Analyze the provided code and generate a visual Mermaid.js sequenceDiagram.

CRITICAL RULES:
1. You MUST output ONLY a valid JSON array of strings. 
2. First element MUST be "sequenceDiagram". Second element MUST be "autonumber".
3. Use ACTUAL class names. DO NOT use generic names like Rule1.
4. Use Mermaid 'box' syntax to group layers (External, API, Service, Rules).
5. AUTOMATIC LOGIC: Carefully identify ALL conditional (if/else/switch) logic in the code and represent them using 'alt', 'else', and 'end' blocks.

COLOR THEMES:
- box rgba(255, 204, 229, 0.5) "External"
- box rgba(230, 245, 255, 0.5) "API Layer"
- box rgba(200, 255, 200, 0.5) "Business Logic"
- box rgba(229, 204, 255, 0.5) "Rules Engine"

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
        return f"Ollama se connect karne mein error: {e}"

def update_markdown_file(content):
    os.makedirs("output", exist_ok=True)
    file_path = "output/api_documentation.md"
    clean_content = content.replace("```markdown", "").replace("```", "").strip()
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(clean_content)
    print(f"✅ SUCCESS: Markdown File update ho gayi -> {file_path}")

def update_mermaid_file(result):
    os.makedirs("output", exist_ok=True)
    file_path = "output/diagram.html"
    
    clean_res = result.replace("```json", "").replace("```mermaid", "").replace("```", "").strip()
    
    try:
        start = clean_res.find('[')
        end = clean_res.rfind(']') + 1
        if start != -1 and end > start:
            json_str = clean_res[start:end]
            diagram_lines = json.loads(json_str)
            clean_res = "\n".join(diagram_lines)
        else:
            raise ValueError("No JSON Array found")
    except Exception as e:
        print(f"⚠️ JSON Parse Fallback chalu hua: {e}")
        
    # Formatting for rendering
    clean_res = clean_res.replace(" participant ", "\nparticipant ")
    clean_res = clean_res.replace(" box ", "\nbox ")
    clean_res = clean_res.replace(" end ", "\nend ")
    clean_res = clean_res.replace(" alt ", "\nalt ")
    clean_res = clean_res.replace(" else ", "\nelse ")
    clean_res = clean_res.replace(" autonumber", "\nautonumber\n")
    clean_res = re.sub(r'\s+([A-Za-z0-9_]+->>)', r'\n\1', clean_res)
    clean_res = re.sub(r'\s+([A-Za-z0-9_]+-->>)', r'\n\1', clean_res)
    clean_res = clean_res.replace("sequenceDiagram", "sequenceDiagram\n")
    clean_res = "\n".join([line.strip() for line in clean_res.split("\n") if line.strip()])

    common_style = """
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #172b4d; max-width: 1200px; margin: 0 auto; padding: 40px; background-color: #f4f5f7; }
        h1 { color: #0052cc; border-bottom: 2px solid #0052cc; padding-bottom: 10px; text-align: center; }
        .mermaid { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; overflow-x: auto; }
    </style>
    """

    content = f"""<!DOCTYPE html>
<html>
<head>
    {common_style}
    <script src="[https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js](https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js)"></script>
</head>
<body>
    <h1>KodeLens - Smart Auto-Generated Flow</h1>
    <div class="mermaid">
{clean_res}
    </div>
    <script>
        const config = {{
            startOnLoad: true, 
            securityLevel: 'loose', 
            theme: 'base',
            themeVariables: {{
                primaryColor: '#e9f2fa',
                primaryTextColor: '#172b4d',
                primaryBorderColor: '#0052cc',
                lineColor: '#6b778c',
                secondaryColor: '#fffae6',
                tertiaryColor: '#e3fcef'
            }}
        }};
        mermaid.initialize(config);
    </script>
</body>
</html>"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ SUCCESS: Visual Diagram update ho gaya -> {file_path}")

# --- MAIN EXECUTION ---
print("Spring Boot Project scan ho raha hai...")
folder = "sample_code"
java_code = read_java_files(folder)

if java_code.strip() == "":
    print(f"Koi Java code nahi mila. '{folder}' folder mein files daaliye.")
else:
    print(f"Java code mil gaya! Processing documentation updates...\n")
    
    print("Aap kya Auto-Update karna chahte hain?")
    print("1. Markdown Documentation (.md)")
    print("2. Visual Sequence Diagram (.html)")
    print("3. Dono Update Karein")
    
    choice = input("Choice (1/2/3): ")
    
    if choice in ['1', '3']:
        print("\nUpdating Markdown Docs...")
        md_result = generate_markdown_docs(java_code)
        if "Error" not in md_result:
            update_markdown_file(md_result)
            
    if choice in ['2', '3']:
        print("\nUpdating Visual Diagram...")
        mermaid_result = generate_mermaid_diagram(java_code)
        if "Error" not in mermaid_result:
            update_mermaid_file(mermaid_result)
            
    print("\nKaam khatam! 'output' folder check karein.")