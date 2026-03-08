# ══════════════════════════════════════════
# PART 6: File Handling + JSON
# AI project mein SABSE zyada use hoga!
# ══════════════════════════════════════════

import json    # Java: import com.fasterxml.jackson.databind.ObjectMapper;
import os      # Java: import java.io.File;

# ─── 1. WRITE A FILE ───
# Java: BufferedWriter bw = new BufferedWriter(new FileWriter("test.txt"));
#       bw.write("Hello"); bw.close();
# Python: 2 lines!
with open("test.txt", "w") as f:
    f.write("Hello Vicky!\n")
    f.write("Python seekh raha hoon!\n")
    f.write("AI Engineer banunga!\n")

print("✅ test.txt written!")

# ─── 2. READ A FILE ───
# Java: BufferedReader br = new BufferedReader(new FileReader("test.txt"));
#       String line; while((line = br.readLine()) != null) { ... }
# Python:
with open("test.txt", "r") as f:
    content = f.read()         # Poora file ek baar mein
print(f"Full content:\n{content}")

# Read line by line
with open("test.txt", "r") as f:
    for line in f:
        print(f"  Line: {line.strip()}")   # strip() removes \n


# ─── 3. READ A JAVA FILE! (AI project mein yahi karenge) ───
# Pehle ek sample Java file banate hain
sample_java = '''package com.example.orders;

import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @GetMapping
    public List<Order> getAllOrders() {
        return orderService.findAll();
    }

    @PostMapping
    public Order createOrder(@RequestBody Order order) {
        return orderService.save(order);
    }

    @GetMapping("/{id}")
    public Order getById(@PathVariable String id) {
        return orderService.findById(id);
    }
}
'''

# Write sample java file
with open("OrderController.java", "w") as f:
    f.write(sample_java)
print("✅ OrderController.java written!")

# Read and analyze it!
with open("OrderController.java", "r") as f:
    for i, line in enumerate(f, 1):
        stripped = line.strip()
        if "@RestController" in stripped:
            print(f"  Line {i}: Found REST Controller!")
        if "@GetMapping" in stripped:
            print(f"  Line {i}: Found GET endpoint!")
        if "@PostMapping" in stripped:
            print(f"  Line {i}: Found POST endpoint!")
        if "class " in stripped:
            print(f"  Line {i}: Found class: {stripped}")

# ─── YE DEKH! Ye hi hai AI project ka core idea! ───
# Java file padho → patterns dhundho → documentation banao!


# ─── 4. JSON — Sabse important! ───
# Java: ObjectMapper mapper = new ObjectMapper();
#       String json = mapper.writeValueAsString(order);

# Python dict → JSON file (Java: mapper.writeValue(file, object))
order_data = {
    "id": "ORD-001",
    "product": "Laptop",
    "quantity": 2,
    "price": 50000,
    "customer": {
        "name": "Vicky",
        "city": "Khatima"
    },
    "items": ["Laptop", "Charger", "Bag"]
}

# Write JSON
with open("order.json", "w") as f:
    json.dump(order_data, f, indent=2)   # indent=2 = pretty print
print("\n✅ order.json written!")

# Read JSON
with open("order.json", "r") as f:
    loaded = json.load(f)                # Java: mapper.readValue(file, Map.class)
print(f"Loaded: {loaded}")
print(f"Product: {loaded['product']}")
print(f"Customer city: {loaded['customer']['city']}")
print(f"First item: {loaded['items'][0]}")


# ─── 5. JSON STRING (API response jaisa) ───
# Java: mapper.readValue(jsonString, Map.class)
json_string = '{"status": "success", "data": {"orderId": "ORD-001", "total": 100000}}'
parsed = json.loads(json_string)         # String → Dict
print(f"\nParsed API response: {parsed}")
print(f"Order ID: {parsed['data']['orderId']}")
print(f"Total: {parsed['data']['total']}")

# Dict → JSON string (for sending to API)
my_dict = {"name": "Vicky", "role": "AI Engineer"}
json_str = json.dumps(my_dict, indent=2)  # Dict → String
print(f"\nDict to JSON:\n{json_str}")


# ─── 6. LIST OF FILES IN FOLDER ───
# Java: File folder = new File("."); File[] files = folder.listFiles();
# Python:
print("\n--- Files in current folder ---")
for filename in os.listdir("."):
    size = os.path.getsize(filename)
    print(f"  {filename} ({size} bytes)")


# ─── SUMMARY ───
print("\n" + "="*50)
print("FILE + JSON CHEAT SHEET")
print("="*50)
print("  Write file:   with open('f.txt', 'w') as f: f.write()")
print("  Read file:    with open('f.txt', 'r') as f: f.read()")
print("  Write JSON:   json.dump(dict, file)")
print("  Read JSON:    json.load(file)")
print("  String→Dict:  json.loads(string)")
print("  Dict→String:  json.dumps(dict)")
print("  List files:   os.listdir('.')")
print("="*50)

