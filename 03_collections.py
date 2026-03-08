# ══════════════════════════════════════════
# PART 3: Python Collections — Java Comparison
# Java mein 15+ types, Python mein bas 4!
# ══════════════════════════════════════════

# ═══════════════════════════════════
# 1. LIST (= ArrayList + LinkedList + Stack sab ek mein!)
# ═══════════════════════════════════

# Java: ArrayList<String> fruits = new ArrayList<>();
fruits = ["apple", "banana", "mango", "apple"]  # duplicates allowed!

fruits.append("orange")          # Java: .add()
fruits.insert(1, "grapes")       # Java: .add(index, element)
fruits.remove("banana")          # Java: .remove("banana")
last = fruits.pop()              # Java: Stack.pop() — removes last
print(f"List: {fruits}")
print(f"Popped: {last}")
print(f"Length: {len(fruits)}")
print(f"'mango' hai? {'mango' in fruits}")  # Java: .contains()

# Sorting
# Java: Collections.sort(fruits)
fruits.sort()
print(f"Sorted: {fruits}")

# Reverse
# Java: Collections.reverse(fruits)
fruits.reverse()
print(f"Reversed: {fruits}")


# ═══════════════════════════════════
# 2. LIST KE ANDAR LIST (Nested List / 2D List)
# Java: List<List<String>>
# ═══════════════════════════════════

# Java: List<List<String>> matrix = new ArrayList<>();
#       List<String> row1 = Arrays.asList("A", "B", "C");

matrix = [
    ["A", "B", "C"],
    ["D", "E", "F"],
    ["G", "H", "I"]
]

print(f"\nFull Matrix: {matrix}")
print(f"Row 0: {matrix[0]}")           # ["A", "B", "C"]
print(f"Row 1, Col 2: {matrix[1][2]}") # "F"  (Java: matrix.get(1).get(2))

# Loop nested list
print("\n--- Matrix Print ---")
for row in matrix:
    for item in row:
        print(f"  {item}", end=" ")
    print()  # new line after each row

# Real Example: Orders with multiple items
orders_with_items = [
    {"id": "ORD-001", "items": ["Laptop", "Mouse", "Keyboard"]},
    {"id": "ORD-002", "items": ["Phone", "Cover"]},
    {"id": "ORD-003", "items": ["Monitor", "Cable", "Stand", "Webcam"]},
]

print("\n--- Orders with Items ---")
for order in orders_with_items:
    print(f"  {order['id']} → {len(order['items'])} items: {order['items']}")


# ═══════════════════════════════════
# 3. TUPLE (= Immutable List, Java mein direct nahi hai)
# ═══════════════════════════════════

# Java: Collections.unmodifiableList(list) jaisa
# Python: Ek baar banao, change nahi kar sakte

coordinates = (28.6139, 77.2090)  # Delhi lat, long
print(f"\nTuple: {coordinates}")
print(f"Latitude: {coordinates[0]}")
print(f"Longitude: {coordinates[1]}")

# coordinates[0] = 100  # ❌ ERROR! Tuple change nahi hota!

# Kab use karo?
# → Jab data fix ho (coordinates, RGB colors, config values)
# → Dict ki key bana sakte ho (list nahi ban sakti key)


# ═══════════════════════════════════
# 4. SET (= HashSet)
# ═══════════════════════════════════

# Java: Set<String> unique = new HashSet<>();
#       unique.add("apple");
unique_fruits = {"apple", "banana", "mango", "apple", "banana"}
print(f"\nSet: {unique_fruits}")  # duplicates automatically hatega!

unique_fruits.add("orange")       # Java: .add()
unique_fruits.discard("banana")   # Java: .remove() — no error if missing
print(f"After changes: {unique_fruits}")
print(f"'mango' hai? {'mango' in unique_fruits}")  # Java: .contains()

# Set operations (Java: retainAll, addAll, removeAll)
set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}

print(f"\nUnion: {set_a | set_b}")          # {1,2,3,4,5,6,7,8} = addAll
print(f"Intersection: {set_a & set_b}")     # {4,5}              = retainAll
print(f"Difference: {set_a - set_b}")       # {1,2,3}            = removeAll

# Real use: Find unique NDCs from orders
all_ndcs = ["NDC-001", "NDC-002", "NDC-001", "NDC-003", "NDC-002", "NDC-001"]
unique_ndcs = set(all_ndcs)
print(f"\nAll NDCs: {all_ndcs} ({len(all_ndcs)} total)")
print(f"Unique NDCs: {unique_ndcs} ({len(unique_ndcs)} unique)")


# ═══════════════════════════════════
# 5. DICT (= HashMap + LinkedHashMap)
# Python 3.7+ mein dict ORDERED hai (LinkedHashMap jaisa!)
# ═══════════════════════════════════

# Java: Map<String, Object> pharmacy = new LinkedHashMap<>();
pharmacy = {
    "id": 39,
    "name": "Greensboro Specialty",
    "state": "NC",
    "hub": True,
    "services": ["mail", "specialty", "retail"]  # list andar dict!
}

print(f"\nPharmacy: {pharmacy}")
print(f"Name: {pharmacy['name']}")
print(f"Services: {pharmacy['services']}")
print(f"First service: {pharmacy['services'][0]}")  # dict → list → item

# Check key exists
# Java: pharmacy.containsKey("hub")
print(f"'hub' key hai? {'hub' in pharmacy}")

# Safe get (no error if key missing)
# Java: pharmacy.getOrDefault("npi", "N/A")
print(f"NPI: {pharmacy.get('npi', 'N/A')}")  # N/A — key nahi hai

# All keys, values
# Java: pharmacy.keySet(), pharmacy.values()
print(f"Keys: {list(pharmacy.keys())}")
print(f"Values: {list(pharmacy.values())}")


# ═══════════════════════════════════
# 6. NESTED DICT (Dict ke andar Dict)
# Java: Map<String, Map<String, Object>>
# Ye SABSE important — API responses aise hi aate hain!
# ═══════════════════════════════════

# Real DP API response jaisa structure:
api_response = {
    "optimal": {
        "pharmacyId": "PH-001",
        "branch": 39,
        "city": "Greensboro",
        "state": "NC",
        "hub": True
    },
    "alternate": {
        "pharmacyId": "PH-002",
        "branch": 42,
        "city": "St. Louis",
        "state": "MO",
        "hub": False
    },
    "temporary": None
}

print("\n--- API Response ---")
print(f"Optimal pharmacy: {api_response['optimal']['city']}, {api_response['optimal']['state']}")
print(f"Optimal branch: {api_response['optimal']['branch']}")
print(f"Alternate pharmacy: {api_response['alternate']['city']}")
print(f"Temporary: {api_response['temporary']}")

# Safe nested access
if api_response['temporary'] is not None:
    print(f"Temp branch: {api_response['temporary']['branch']}")
else:
    print("No temporary pharmacy assigned")


# ═══════════════════════════════════
# SUMMARY TABLE
# ═══════════════════════════════════
print("\n" + "="*50)
print("JAVA → PYTHON COLLECTIONS CHEAT SHEET")
print("="*50)
print(f"  ArrayList    → list    = {[1, 2, 3]}")
print(f"  LinkedList   → list    = same!")
print(f"  HashSet      → set     = {'{1, 2, 3}'}")
print(f"  HashMap      → dict    = {'{\"a\": 1}'}")
print(f"  Immutable    → tuple   = {(1, 2, 3)}")
print(f"  int[]        → list    = {[1, 2, 3]}")
print("="*50)
