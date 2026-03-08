import json

# Dict bana
profile = {
    "name": "Vishawanath Singh",
    "age": 34,
    "role": "Senior Software Engineer",
    "salary": 1900000,
    "skills": ["Java", "Spring Boot", "Python", "LangChain", "RAG"],
    "projects": [
        {"name": "DP API", "tech": "Spring Boot", "company": "Express Scripts"},
        {"name": "AI Architecture Analyzer", "tech": "Python + Ollama", "company": "Personal"}
    ]
}

# JSON file mein save karo
with open("profile.json", "w") as f:
    json.dump(profile, f, indent=2)
print("profile.json saved!")

# JSON file se padho
with open("profile.json", "r") as f:
    loaded = json.load(f)

# Data access karo
print(f"Name: {loaded['name']}")
print(f"First skill: {loaded['skills'][0]}")
print(f"First project: {loaded['projects'][0]['name']}")
print(f"All skills: {', '.join(loaded['skills'])}")

# Saare projects print karo
print("\n--- Projects ---")
for project in loaded['projects']:
    print(f"  {project['name']} ({project['tech']}) at {project['company']}")