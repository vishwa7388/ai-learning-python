# ============================================
# orchestrator.py — Controller + Main Entry Point
# Coordinates: Scanner → Prompt Builder → AI Client → Save Output
# Java Analogy: Like Controller — receives request (CLI args),
#               calls Service layer, returns response (saved files)
# 
# USAGE:
#   python orchestrator.py --folder path/to/java/src --all
#   python orchestrator.py --folder path/to/java/src --hld --lld
#   python orchestrator.py --folder path/to/java/src --diagram --audit
# ============================================

import os
import re
import json
import argparse

# --- Import our modules (like @Autowired in Spring Boot!) ---
from code_scanner import scan_folder, get_project_structure, print_structure, read_all_code, read_java_file
from prompt_builder import (
    build_docs_prompt, build_html_prompt, build_hld_prompt, build_lld_prompt,
    build_mermaid_prompt, build_flow_prompt, build_audit_prompt, build_smart_prompt
)
from ai_client import call_ai


# --- CLI Arguments (like @RequestParam in Controller) ---
def get_args():
    parser = argparse.ArgumentParser(description="KodeLens - AI Code Documentation Tool")
    parser.add_argument("--folder", default="sample_code", help="Project folder path")
    parser.add_argument("--docs", action="store_true", help="Generate Markdown docs")
    parser.add_argument("--html", action="store_true", help="Generate HTML docs")
    parser.add_argument("--diagram", action="store_true", help="Generate Mermaid diagram")
    parser.add_argument("--flow", action="store_true", help="Generate connected flow")
    parser.add_argument("--audit", action="store_true", help="Security audit")
    parser.add_argument("--smart", action="store_true", help="Smart analysis per file")
    parser.add_argument("--hld", action="store_true", help="Generate high-level design")
    parser.add_argument("--lld", action="store_true", help="Generate low-level design")
    parser.add_argument("--all", action="store_true", help="Generate everything")
    return parser.parse_args()


# --- Save Functions (like Response builders) ---
def save_markdown(content, filename):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"
    clean = content.replace("```markdown", "").replace("```", "").strip()
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(clean)
    print(f"  Saved: {filepath}")


def save_html_doc(content, filename):
    os.makedirs("output", exist_ok=True)
    filepath = f"output/{filename}"

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

    print(f"  Saved: {filepath}")


# --- Smart Analysis (loops through each file) ---
def run_smart_analysis(files, structure):
    results = {}
    for category, file_list in structure.items():
        for file_path in file_list:
            filename = os.path.basename(file_path)
            code = read_java_file(file_path)
            if code is None:
                continue

            prompt = build_smart_prompt(category, code, filename)
            print(f"    Analyzing [{category.upper()}]: {filename}")
            result = call_ai(prompt)
            if result:
                results[filename] = {
                    "category": category,
                    "analysis": result
                }
    return results


# --- MAIN — The Controller method ---
def main():
    print("\n" + "=" * 50)
    print("  KodeLens - AI Code Documentation Tool")
    print("  Version 2.0 (Refactored)")
    print("=" * 50)

    # 1. Parse CLI args (like reading @RequestParam)
    args = get_args()
    folder = args.folder

    # 2. Scan files (like calling Repository)
    files = scan_folder(folder)
    if not files:
        print("  No Java files found!")
        return

    structure = get_project_structure(files)
    print_structure(structure)

    # 3. Read all code
    all_code = read_all_code(files)

    # 4. Default to --all if nothing specified
    if not any([args.docs, args.html, args.diagram, args.flow,
                args.audit, args.smart, args.hld, args.lld, args.all]):
        args.all = True

    print("\nGenerating...\n")

    # 5. Generate each doc type:
    #    prompt_builder builds prompt → ai_client calls AI → save result
    #    (Service builds query → WebClient calls API → Controller saves response)

    if args.docs or args.all:
        print("  [1] API Documentation (Markdown)...")
        prompt = build_docs_prompt(all_code)       # Service layer
        result = call_ai(prompt)                    # WebClient layer
        if result:
            save_markdown(result, "api_documentation.md")

    if args.html or args.all:
        print("  [2] API Documentation (HTML)...")
        prompt = build_html_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_html_doc(result, "api_documentation.html")

    if args.diagram or args.all:
        print("  [3] Flow Diagram (Mermaid)...")
        prompt = build_mermaid_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_mermaid_html(result)

    if args.flow or args.all:
        print("  [4] Connected Flow...")
        prompt = build_flow_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_markdown(result, "connected_flow.md")

    if args.audit or args.all:
        print("  [5] Security Audit...")
        prompt = build_audit_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_markdown(result, "security_audit.md")

    if args.smart or args.all:
        print("  [6] Smart Analysis...")
        results = run_smart_analysis(files, structure)
        if results:
            save_smart_report(results)

    if args.hld or args.all:
        print("  [7] High Level Design (HLD)...")
        prompt = build_hld_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_markdown(result, "hld_document.md")

    if args.lld or args.all:
        print("  [8] Low Level Design (LLD)...")
        prompt = build_lld_prompt(all_code)
        result = call_ai(prompt)
        if result:
            save_markdown(result, "lld_document.md")

    print("\n" + "=" * 50)
    print("  DONE! Check output/ folder")
    print("=" * 50)


if __name__ == "__main__":
    main()