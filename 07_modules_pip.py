# ══════════════════════════════════════════
# PART 7: Modules + pip (LAST PART!)
# Java: import + Maven → Python: import + pip
# ══════════════════════════════════════════

# ─── 1. BUILT-IN MODULES (Java: java.util, java.io) ───
import os
import sys
import datetime
import re          # regex

# os — system info
print(f"Current folder: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"OS: {os.name}")

# datetime — date/time
# Java: LocalDateTime.now()
now = datetime.datetime.now()
print(f"\nDate: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# re — regex (AI project mein bohot use hoga!)
# Java: Pattern.compile("@GetMapping").matcher(text).find()
text = "@GetMapping('/api/orders')"
match = re.search(r"@(\w+Mapping)", text)
if match:
    print(f"\nFound annotation: {match.group(1)}")

# Multiple patterns
java_code = """
@RestController
@RequestMapping("/api/orders")
@GetMapping("/{id}")
@PostMapping
@DeleteMapping("/{id}")
"""
annotations = re.findall(r"@(\w+Mapping)", java_code)
print(f"All annotations: {annotations}")


# ─── 2. YOUR OWN MODULE ───
# Java: import com.example.utils.OrderUtils;
# Python: import filename (without .py)

# Hum ek helper module banayenge — pehle file create karte hain
helper_code = '''
def format_price(amount):
    return f"Rs.{amount:,.2f}"

def generate_id(prefix, number):
    return f"{prefix}-{number:03d}"

ORDER_STATUS = ["PENDING", "CONFIRMED", "SHIPPED", "DELIVERED"]
'''

with open("my_helpers.py", "w") as f:
    f.write(helper_code)

# Ab use karo!
import my_helpers

print(f"\nFormatted: {my_helpers.format_price(50000)}")
print(f"ID: {my_helpers.generate_id('ORD', 42)}")
print(f"Statuses: {my_helpers.ORDER_STATUS}")

# Specific import
from my_helpers import format_price, generate_id
print(f"Direct use: {format_price(123456)}")


# ─── 3. PIP = Maven/Gradle of Python ───
# Java:  pom.xml → <dependency>...</dependency> → mvn install
# Python: pip install library_name
#
# Terminal mein ye chalao (ye file mein nahi, TERMINAL mein!):
#   pip install requests
#
# Popular libraries we'll use in AI project:
#   pip install requests      → API calls (Java: RestTemplate)
#   pip install langchain     → AI framework
#   pip install chromadb      → Vector database (RAG)

print("\n" + "="*50)
print("MODULES CHEAT SHEET")
print("="*50)
print("  import os              = import java.io.*")
print("  import json            = import jackson")
print("  import re              = import java.util.regex")
print("  from x import y        = import com.x.Y")
print("  pip install requests   = Maven dependency add")
print("  requirements.txt       = pom.xml")
print("="*50)

print("\n🎉 PYTHON BASICS COMPLETE! 🎉")
print("Tu ab Python likh sakta hai!")
print("Kal se Practice + Spring Boot + AI shuru!")



#Phir terminal mein ek aur command:

#pip install requests
