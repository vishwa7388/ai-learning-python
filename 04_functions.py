# ══════════════════════════════════════════
# PART 4: Functions (Java: Methods)
# ══════════════════════════════════════════

# ─── 1. BASIC FUNCTION ───
# Java: public void greet(String name) { System.out.println("Hello " + name); }
# Python:
def greet(name):
    print(f"Hello {name}!")

greet("Vicky")
greet("Dillon")


# ─── 2. RETURN VALUE ───
# Java: public int add(int a, int b) { return a + b; }
# Python:
def add(a, b):
    return a + b

result = add(10, 20)
print(f"10 + 20 = {result}")


# ─── 3. DEFAULT PARAMETER ───
# Java: Method overloading chahiye (2 methods)
# Python: Ek function, default value do!
def create_order(product, quantity=1, discount=0):
    total = quantity * 100 - discount
    return {"product": product, "qty": quantity, "discount": discount, "total": total}

order1 = create_order("Laptop")              # quantity=1, discount=0 automatic
order2 = create_order("Mouse", 5)            # quantity=5, discount=0
order3 = create_order("Keyboard", 3, 50)     # quantity=3, discount=50
print(f"\nOrder 1: {order1}")
print(f"Order 2: {order2}")
print(f"Order 3: {order3}")


# ─── 4. MULTIPLE RETURN ───
# Java: Ek hi return hota hai (ya Object/Array banana padta)
# Python: Multiple values return kar sakte ho!
def get_min_max(numbers):
    return min(numbers), max(numbers)

smallest, largest = get_min_max([45, 12, 89, 3, 67])
print(f"\nSmallest: {smallest}, Largest: {largest}")


# ─── 5. LIST AS PARAMETER ───
# Java: public void processOrders(List<Map<String,Object>> orders)
# Python:
def calculate_total(orders):
    total = 0
    for order in orders:
        total += order["price"] * order["qty"]
    return total

my_orders = [
    {"product": "Laptop", "price": 50000, "qty": 1},
    {"product": "Mouse", "price": 500, "qty": 2},
    {"product": "Keyboard", "price": 1500, "qty": 1},
]
print(f"\nTotal bill: Rs.{calculate_total(my_orders)}")


# ─── 6. LAMBDA (Java: Arrow Function) ───
# Java: (a, b) -> a + b
# Python:
add_lambda = lambda a, b: a + b
print(f"\nLambda add: {add_lambda(5, 3)}")

# Real use: Sorting
products = [
    {"name": "Laptop", "price": 50000},
    {"name": "Mouse", "price": 500},
    {"name": "Monitor", "price": 25000},
]

# Java: products.sort((a,b) -> a.getPrice().compareTo(b.getPrice()))
products.sort(key=lambda p: p["price"])
print(f"Sorted by price: {[p['name'] for p in products]}")
