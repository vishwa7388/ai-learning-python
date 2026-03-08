# ══════════════════════════════════════════
# PART 2: Lists & Dictionaries
# Java: ArrayList & HashMap → Python mein EASY!
# ══════════════════════════════════════════

# ─── 1. LIST (Java: ArrayList) ───
# Java:  List<String> orders = new ArrayList<>();
#        orders.add("ORD-001");
# Python:
orders = ["ORD-001", "ORD-002", "ORD-003"]

orders.append("ORD-004")       # Java: orders.add()
print(f"All orders: {orders}")
print(f"First: {orders[0]}")   # Java: orders.get(0)
print(f"Last: {orders[-1]}")   # Python special! -1 = last item
print(f"Total: {len(orders)}") # Java: orders.size()

# ─── 2. LIST SLICING (Java mein nahi hota!) ───
print(f"First 2: {orders[:2]}")    # [ORD-001, ORD-002]
print(f"Last 2: {orders[-2:]}")    # [ORD-003, ORD-004]

# ─── 3. LOOP ON LIST ───
# Java:  for(String order : orders) { System.out.println(order); }
# Python:
print("\n--- All Orders ---")
for order in orders:
    print(f"  Order: {order}")

# ─── 4. LOOP WITH INDEX ───
# Java:  for(int i=0; i<orders.size(); i++)
# Python: enumerate
print("\n--- With Index ---")
for i, order in enumerate(orders):
    print(f"  {i+1}. {order}")

# ─── 5. LIST COMPREHENSION (Java: Stream + Collect) ───
# Java:  orders.stream().filter(o -> o.contains("002")).collect(Collectors.toList())
# Python: EK LINE mein!
filtered = [o for o in orders if "002" in o]
print(f"\nFiltered: {filtered}")

# ─── 6. DICTIONARY (Java: HashMap) ───
# Java:  Map<String, Object> order = new HashMap<>();
#        order.put("id", "ORD-001");
# Python:
order = {
    "id": "ORD-001",
    "product": "Laptop",
    "quantity": 2,
    "price": 50000.00,
    "delivered": False
}

print(f"\nOrder: {order}")
print(f"Product: {order['product']}")   # Java: order.get("product")
print(f"Price: {order['price']}")

# ─── 7. ADD/UPDATE DICT ───
# Java:  order.put("discount", 10)
order["discount"] = 10
order["price"] = 45000.00    # update existing
print(f"Updated: {order}")

# ─── 8. LOOP ON DICT ───
# Java:  for(Map.Entry<String,Object> e : order.entrySet())
print("\n--- Order Details ---")
for key, value in order.items():
    print(f"  {key}: {value}")

# ─── 9. LIST OF DICTS (Java: List<Map>) ───
# Real world mein data aise hi aata hai — like API response!
all_orders = [
    {"id": "ORD-001", "product": "Laptop", "price": 50000},
    {"id": "ORD-002", "product": "Mouse", "price": 500},
    {"id": "ORD-003", "product": "Keyboard", "price": 1500},
    {"id": "ORD-004", "product": "Monitor", "price": 25000},
]

print("\n--- Order Summary ---")
total = 0
for o in all_orders:
    print(f"  {o['id']}: {o['product']} - Rs.{o['price']}")
    total += o['price']
print(f"  TOTAL: Rs.{total}")

# ─── 10. FILTER EXPENSIVE (price > 5000) ───
expensive = [o for o in all_orders if o['price'] > 5000]
print(f"\nExpensive orders (>5000): {[o['product'] for o in expensive]}")

