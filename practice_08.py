# File banao (write)
with open("my_profile.txt", "w") as f:
    f.write("Name: Vishawanath Singh\n")
    f.write("Age: 34\n")
    f.write("Role: Senior Software Engineer\n")
    f.write("Skills: Java, Spring Boot, Python, AI\n")
    f.write("Goal: AI Engineer in 2 months!\n")

print("File created!")

# File padho (read) — poora ek saath
with open("my_profile.txt", "r") as f:
    content = f.read()

print("\n--- Full Content ---\n")
print(content)

# Line by line padho with numbers
with open("my_profile.txt", "r") as f:
    count = 0
    for line in f:
        count += 1
        print(f"Line {count}: {line.strip()}")