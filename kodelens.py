import requests
import os
import json
import re
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="KodeLens - AI Code Documentation Tool")
    parser.add_argument("--folder", default="sample_code", help="Project folder path")
    parser.add_argument("--docs", action="store_true", help="Generate Markdown docs")
    parser.add_argument("--html", action="store_true", help="Generate HTML docs")
    parser.add_argument("--diagram", action="store_true", help="Generate Mermaid diagram")
    parser.add_argument("--flow", action="store_true", help="Generate connected flow")
    parser.add_argument("--audit", action="store_true", help="Security audit")
    parser.add_argument("--smart", action="store_true", help="Smart analysis per file")
    parser.add_argument("--hld", action="store_true", help="Generate high-level design (Markdown)")
    parser.add_argument("--lld", action="store_true", help="Generate low-level design (Markdown)")
    parser.add_argument("--all", action="store_true", help="Generate everything")
    return parser.parse_args()
# ============================================
# KodeLens - AI Code Documentation Tool
# Version: 1.0
# ============================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"
TIMEOUT = 600

# --- FILE READING ---
def read_java_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"ERROR: {file_path} - {e}")
        return None

def scan_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder '{folder_path}' nahi mila!")
        return []

    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files

# --- FILE CATEGORIZATION ---
def categorize_file(filename, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(500)
    except:
        return "other"

    lower_name = filename.lower()

    if "controller" in lower_name or "@RestController" in content or "@Controller" in content:
        return "controllers"
    elif "service" in lower_name or "@Service" in content:
        return "services"
    elif "adaptor" in lower_name or "adapter" in lower_name:
        return "adaptors"
    elif "rule" in lower_name:
        return "rules"
    elif "model" in lower_name or "dto" in lower_name or "request" in lower_name or "response" in lower_name:
        return "models"
    elif "config" in lower_name or "@Configuration" in content:
        return "config"
    return "other"

def get_project_structure(files):
    structure = {
        "controllers": [],
        "services": [],
        "adaptors": [],
        "rules": [],
        "models": [],
        "config": [],
        "other": []
    }

    for file_path in files:
        filename = os.path.basename(file_path)
        category = categorize_file(filename, file_path)
        structure[category].append(file_path)

    return structure

def print_structure(structure):
    print("\n" + "=" * 50)
    print("PROJECT STRUCTURE")
    print("=" * 50)

    for category, files in structure.items():
        if files:
            print(f"\n  {category.upper()} ({len(files)} files):")
            for f in files:
                print(f"    - {os.path.basename(f)}")

    total = sum(len(f) for f in structure.values())
    print(f"\n  Total Java files: {total}")
    print("=" * 50)

# --- AI CALL ---
def call_ai(prompt):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=TIMEOUT)
        return response.json().get("response", "")
    except requests.exceptions.ConnectionError:
        print("ERROR: Ollama not running! Start with: ollama serve")
        return None
    except Exception as e:
        print(f"ERROR: AI call failed - {e}")
        return None

# --- SMART PROMPTS (Different per file type) ---
def get_smart_prompt(category, code, filename):
    prompts = {
        "controllers": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this REST Controller.
FORMAT:
- Endpoint URL and HTTP Method
- Request Body fields
- Response Body fields
- Which Service it calls
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "services": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Service class and trace the business flow.
FORMAT:
- Purpose (1 line)
- Step-by-step business logic flow
- External calls made (which Adaptors)
- Business rules applied
- Return value
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "adaptors": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Adaptor/Client class.
FORMAT:
- External API URL it calls
- HTTP Method used
- Request parameters
- Response type
- Error handling
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "rules": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Business Rule class.
FORMAT:
- Rule Name
- What it checks
- Input parameters
- Decision logic
- Impact on pharmacy routing
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "models": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this model/DTO class.
FORMAT:
- Purpose
- Fields (name and type)
- Used as Request or Response
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "config": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this configuration class.
FORMAT:
- What it configures
- Beans defined
- Properties used
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}"""
    }

    return prompts.get(category, prompts["services"])

# --- GENERATORS ---

# 1. Full Documentation (Markdown)
def generate_docs(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice.

TASK: Generate complete API documentation.

FORMAT (Markdown):
## 1. Overview
(What does this API do - 2 lines max)

## 2. Entry Point
(Controller, endpoint, HTTP method)

## 3. Request
(What fields come in the request)

## 4. Processing Flow
Step 1: ...
Step 2: ...

## 5. External API Calls
| API Name | Purpose | Called From |
|----------|---------|-------------|

## 6. Business Rules
(List each rule and what it does)

## 7. Response
(What fields go back in response)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""

    return call_ai(prompt)

def generate_hld(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes high-level design documents.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice.

TASK: Produce a concise high-level design from the codebase.

FORMAT (Markdown only). Use exactly these ## section headings in order:

## System Overview
(2 lines max: what the system does and its main boundary)

## Architecture Layers
Describe how code maps to: Controller, Service, Adaptor (or Adapter), Model layers. Use bullets or short paragraphs.

## Component Responsibilities
| Component | Layer | Responsibility |
|-----------|-------|----------------|
(One row per significant class or package; infer from code)

## External Systems and APIs
| System/API | Purpose | Called From |
|------------|---------|-------------|
(HTTP clients, RSS, DB, message queues, third-party URLs, etc.—only what appears in code)

## Tech Stack
(Bullet list: language, framework, key libraries, build tool—only what is evidenced by the code)

## Data Flow Summary
(Short numbered or bulleted summary: request in → layers → external calls → response out)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep tables aligned and readable.

CODE:
{all_code}"""

    return call_ai(prompt)

def generate_lld(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes low-level design documents.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice.

TASK: Produce a low-level design from the codebase: class-by-class detail grounded in the actual code.

FORMAT (Markdown only). For each public or significant class, use this structure (repeat per class):

## <ClassName>
### Key fields / attributes
(Bullet list: field name, type, brief role—only members that matter for behavior or API contracts)

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
(One row per non-trivial method; include constructors if they encode important wiring)

### Dependencies
(Bullets: which other classes this class calls or injects—caller → callee)

Also include one top section before the per-class blocks:

## Class dependency overview
(Short table or bullet list summarizing which class calls which across the project)

Skip boilerplate getters/setters unless they encode business meaning.
Do NOT explain annotations or Spring Boot basics.
Do NOT repeat the same method or field twice. Keep tables aligned and readable.

CODE:
{all_code}"""

    return call_ai(prompt)

# 2. Full Documentation (HTML)
def generate_docs_html(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice.

TASK: Generate complete API documentation.

FORMAT:
Generate output in clean HTML format.
Use <h2> for sections, <table> for tables, <ol> for steps.
Do NOT use Markdown. Use only HTML tags.
OUTPUT ONLY HTML TAGS. No Markdown symbols like # or ** or ```. Only use <h2>, <p>, <table>, <ol> tags.

Sections:
1. Overview (2 lines max)
2. Entry Point (Controller, endpoint, HTTP method)
3. Request (fields)
4. Processing Flow (step by step)
5. External API Calls (table: API Name, Purpose, Called From)
6. Business Rules (list each rule)
7. Response (fields)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""

    return call_ai(prompt)

def generate_mermaid(all_code):
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
{all_code}"""

    return call_ai(prompt)

# 4. Connected Flow
def generate_flow(all_code):
    prompt = f"""ROLE: You are a Senior Spring Boot architect.

CONTEXT: These files are part of Dispensing Pharmacies API - a pharmacy routing microservice.

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

    return call_ai(prompt)

# 5. Security Audit
def generate_security_audit(all_code):
    prompt = f"""ROLE: You are a Cyber Security Expert specializing in Spring Boot applications.

TASK: Analyze this code for security vulnerabilities.

FORMAT:
## Security Findings

For each finding:
- Severity: HIGH / MEDIUM / LOW
- Location: (which file, which line/method)
- Issue: (what is the problem)
- Fix: (how to fix it)

Check for:
- SQL Injection
- Missing input validation
- Hardcoded credentials
- Missing authentication
- Insecure API calls (HTTP vs HTTPS)
- Missing error handling that leaks info
- Missing rate limiting

Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""

    return call_ai(prompt)

# 6. Smart Analysis (Different prompt per file type)
def generate_smart_analysis(files, structure):
    results = {}

    for category, file_list in structure.items():
        for file_path in file_list:
            filename = os.path.basename(file_path)
            code = read_java_file(file_path)
            if code is None:
                continue

            prompt = get_smart_prompt(category, code, filename)
            print(f"  Analyzing [{category.upper()}]: {filename}")
            result = call_ai(prompt)

            if result:
                results[filename] = {
                    "category": category,
                    "analysis": result
                }

    return results

# --- SAVE FUNCTIONS ---
def save_markdown(content, filename):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"
    clean = content.replace("```markdown", "").replace("```", "").strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean)

    print(f"  Saved: {filepath}")

def save_hld(content):
    os.makedirs("output", exist_ok=True)
    filepath = "output/hld_document.md"
    clean = content.replace("```markdown", "").replace("```", "").strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean)

    print(f"  Saved: {filepath}")

def save_lld(content):
    os.makedirs("output", exist_ok=True)
    filepath = "output/lld_document.md"
    clean = content.replace("```markdown", "").replace("```", "").strip()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean)

    print(f"  Saved: {filepath}")

def save_html_doc(content, filename):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"

    # Convert Markdown to HTML
    clean = content.replace("```markdown", "").replace("```mermaid", "").replace("```", "").strip()
    clean = re.sub(r'^## (.+)$', r'<h2>\1</h2>', clean, flags=re.MULTILINE)
    clean = re.sub(r'^# (.+)$', r'<h1>\1</h1>', clean, flags=re.MULTILINE)
    clean = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', clean)
    clean = re.sub(r'^\- (.+)$', r'<li>\1</li>', clean, flags=re.MULTILINE)
    clean = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', clean, flags=re.MULTILINE)
    clean = clean.replace("\n\n", "</p><p>")
    clean = f"<p>{clean}</p>"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f4f5f7; padding: 40px; max-width: 900px; margin: 0 auto; }}
        h1 {{ color: #0052cc; border-bottom: 2px solid #0052cc; padding-bottom: 10px; }}
        h2 {{ color: #172b4d; margin-top: 30px; }}
        li {{ line-height: 1.8; }}
        p {{ line-height: 1.6; }}
        strong {{ color: #0052cc; }}
    </style>
</head>
<body>
    <h1>KodeLens - API Documentation</h1>
    {clean}
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Saved: {filepath}")

def save_mermaid_html(result):
    os.makedirs("output", exist_ok=True)
    filepath = "output/flow_diagram.html"

    raw = result.replace("```json", "").replace("```mermaid", "").replace("```", "").strip()
    clean = ""

    try:
        start = raw.find('[')
        end = raw.rfind(']') + 1
        if start != -1 and end > start:
            json_str = raw[start:end]
            diagram_lines = json.loads(json_str)
            clean = "\n".join(diagram_lines)
        else:
            clean = raw
    except:
        clean = raw

    clean = re.sub(r'\bsequenceDiagram\b', 'sequenceDiagram\n', clean)
    keywords = ["autonumber", "participant", "box", "alt", "else", "end", "rect", "loop"]
    for kw in keywords:
        clean = re.sub(rf'(?<!\n)\s*\b({kw})\b', rf'\n\1', clean)
    clean = re.sub(r'(?<!\n)\s*(\S+[-]{1,2}>>)', r'\n\1', clean)

    lines = []
    for line in clean.split('\n'):
        l = line.strip().strip('"').strip("'").strip(',').strip()
        if l and l.lower() != "null":
            if "participant" in l and "->" in l:
                sub_parts = re.split(r'(?=->|-->>)', l)
                for sp in sub_parts:
                    if sp.strip():
                        lines.append(sp.strip())
            else:
                lines.append(l)

    final = "\n".join(lines)
    final = final.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f4f5f7; padding: 40px; }}
        h1 {{ color: #0052cc; text-align: center; border-bottom: 2px solid #0052cc; padding-bottom: 10px; }}
        .mermaid {{
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            max-width: 95%;
            margin: 20px auto;
            overflow-x: auto;
            white-space: pre;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
    <h1>KodeLens - Service Flow Diagram</h1>
    <div class="mermaid">
{final}
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

    with open("output/flow_diagram.mmd", "w", encoding="utf-8") as f:
        f.write(final)
    print(f"  Saved: output/flow_diagram.mmd")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Saved: {filepath}")

def save_smart_report(results):
    os.makedirs("output", exist_ok=True)
    filepath = "output/smart_analysis_report.md"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# KodeLens - Smart Project Analysis Report\n\n")
        f.write(f"**Total Files Analyzed:** {len(results)}\n\n")
        f.write("---\n\n")

        categories = {}
        for filename, data in results.items():
            cat = data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((filename, data["analysis"]))

        for category, file_list in categories.items():
            f.write(f"## {category.upper()}\n\n")
            for filename, analysis in file_list:
                f.write(f"### {filename}\n\n")
                f.write(analysis.replace("```", "").strip())
                f.write("\n\n---\n\n")


# --- MAIN ---
def main():
    print("\n" + "=" * 50)
    print("  KodeLens - AI Code Documentation Tool")
    print("  Version 1.0")
    print("=" * 50)

    args = get_args()
    folder = args.folder

    files = scan_folder(folder)
    if not files:
        print("No Java files found!")
        return

    structure = get_project_structure(files)
    print_structure(structure)

    # Read all code
    all_code = ""
    for file_path in files:
        filename = os.path.basename(file_path)
        code = read_java_file(file_path)
        if code:
            all_code += f"\n// --- FILE: {filename} ---\n{code}\n"

    if not any([args.docs, args.html, args.diagram, args.flow, args.audit, args.smart, args.hld, args.lld, args.all]):
        args.all = True

    print("\nGenerating...\n")

    if args.docs or args.all:
        print("[1] API Documentation (Markdown)...")
        result = generate_docs(all_code)
        if result:
            save_markdown(result, "api_documentation.md")

    if args.html or args.all:
        print("[2] API Documentation (HTML)...")
        result = generate_docs_html(all_code)
        if result:
            save_html_doc(result, "api_documentation.html")

    if args.diagram or args.all:
        print("[3] Flow Diagram (Mermaid)...")
        result = generate_mermaid(all_code)
        if result:
            save_mermaid_html(result)

    if args.flow or args.all:
        print("[4] Connected Flow...")
        result = generate_flow(all_code)
        if result:
            save_markdown(result, "connected_flow.md")

    if args.audit or args.all:
        print("[5] Security Audit...")
        result = generate_security_audit(all_code)
        if result:
            save_markdown(result, "security_audit.md")

    if args.smart or args.all:
        print("[6] Smart Analysis...")
        results = generate_smart_analysis(files, structure)
        if results:
            save_smart_report(results)

    if args.hld or args.all:
        print("[7] High Level Design (HLD)...")
        result = generate_hld(all_code)
        if result:
            save_hld(result)

    if args.lld or args.all:
        print("[8] Low Level Design (LLD)...")
        result = generate_lld(all_code)
        if result:
            save_lld(result)

    print("\n" + "=" * 50)
    print("  DONE! Check output/ folder")
    print("=" * 50)

if __name__ == "__main__":
    main()