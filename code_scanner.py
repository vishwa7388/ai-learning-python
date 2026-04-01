# ============================================
# code_scanner.py — Repository Layer
# Reads and categorizes Java source files
# Java Analogy: Like a Repository — only reads data, no processing
# ============================================

import os


def read_java_file(file_path):
    """Single Java file ka code padhta hai — like repository.findById()"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  ERROR: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"  ERROR: {file_path} - {e}")
        return None


def scan_folder(folder_path):
    """Folder mein se saari .java files dhundta hai — like repository.findAll()"""
    if not os.path.exists(folder_path):
        print(f"  ERROR: Folder '{folder_path}' not found!")
        return []

    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files


def categorize_file(filename, file_path):
    """File ko uske type ke hisaab se categorize karta hai — Controller, Service, etc."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(500)  # Pehle 500 chars enough hain annotation check ke liye
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
    """Saari files ko categories mein organize karta hai — like a grouped query result"""
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
    """Project structure ko console pe print karta hai"""
    print("\n" + "=" * 50)
    print("  PROJECT STRUCTURE")
    print("=" * 50)

    for category, files in structure.items():
        if files:
            print(f"\n  {category.upper()} ({len(files)} files):")
            for f in files:
                print(f"    - {os.path.basename(f)}")

    total = sum(len(f) for f in structure.values())
    print(f"\n  Total Java files: {total}")
    print("=" * 50)


def read_all_code(files):
    """Saari files ka code ek string mein combine karta hai — like a batch read"""
    all_code = ""
    for file_path in files:
        filename = os.path.basename(file_path)
        code = read_java_file(file_path)
        if code:
            all_code += f"\n// --- FILE: {filename} ---\n{code}\n"
    return all_code