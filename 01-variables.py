# ══════════════════════════════════════════
# PYTHON BASICS — PART 1: Variables
# Java dev ke liye — har line mein comparison
# ══════════════════════════════════════════

# ─── 1. VARIABLES ───
# Java:  String name = "Vicky";
# Python: Bas likho, type ki zaroorat nahi!
name = "Vicky"
age = 28
is_developer = True
salary = 25000.50

print(name)
print(age)
print(is_developer)
print(salary)

# ─── 2. TYPE CHECK ───
# Java:  instanceof
# Python: type()
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
print(type(is_developer))  # <class 'bool'>
print(type(salary))     # <class 'float'>

# ─── 3. STRING FORMATTING (f-string) ───
# Java:  String.format("Name: %s, Age: %d", name, age)
# Python: f-string — bohot easy!
print(f"Name: {name}, Age: {age}")
print(f"Salary: {salary}")
print(f"Developer: {is_developer}")

# ─── 4. STRING METHODS ───
# Java:  name.toUpperCase()
# Python: name.upper()
print(name.upper())        # VICKY
print(name.lower())        # vicky
print(name.startswith("V"))  # True
print(len(name))            # 5  (Java: name.length())

# ─── 5. MULTIPLE ASSIGNMENT ───
# Java mein nahi hota!
# Python mein ek line mein multiple variables!
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")

# ─── 6. INPUT FROM USER ───
# Java:  Scanner sc = new Scanner(System.in); String input = sc.nextLine();
# Python: Ek line!
user_name = input("Tera naam bata: ")
print(f"Welcome {user_name}! Python seekh raha hai tu!")


