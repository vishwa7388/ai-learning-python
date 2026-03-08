# ══════════════════════════════════════════
# PART 5: OOP (Classes) — Java Dev ke liye
# Java mein 50 lines, Python mein 15 lines!
# ══════════════════════════════════════════

# ─── 1. BASIC CLASS ───
# Java:
#   public class Order {
#       private String id;
#       private String product;
#       private int quantity;
#       public Order(String id, String product, int quantity) {
#           this.id = id; this.product = product; this.quantity = quantity;
#       }
#       public String getId() { return id; }
#       // ... getter setter for each field
#       @Override public String toString() { return "Order{id=" + id + "}"; }
#   }

# Python: BAS ITNA!
class Order:
    def __init__(self, id, product, quantity, price):
        self.id = id                # Java: this.id = id
        self.product = product
        self.quantity = quantity
        self.price = price

    def __str__(self):              # Java: toString()
        return f"Order({self.id}: {self.product} x{self.quantity})"

# Create object
# Java: Order order = new Order("ORD-001", "Laptop", 2, 50000);
# Python: new keyword nahi lagta!
order = Order("ORD-001", "Laptop", 2, 50000)
print(order)                        # __str__ automatically call hota hai
print(f"Product: {order.product}")  # Java: order.getProduct() — no getter needed!
order.quantity = 5                  # Java: order.setQuantity(5) — no setter needed!
print(f"Updated qty: {order.quantity}")


# ─── 2. METHODS IN CLASS ───
# Java: public double getTotal() { return quantity * price; }
# Python:
class OrderWithMethods:
    def __init__(self, id, product, quantity, price):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.price = price

    def get_total(self):            # Java: getTotal() — self = this
        return self.quantity * self.price

    def apply_discount(self, percent):
        discount = self.get_total() * percent / 100
        self.price = self.price - (discount / self.quantity)
        return discount

    def to_dict(self):              # Java: like toMap()
        return {
            "id": self.id,
            "product": self.product,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.get_total()
        }

    def __str__(self):
        return f"{self.id}: {self.product} x{self.quantity} = Rs.{self.get_total()}"

o = OrderWithMethods("ORD-002", "Monitor", 2, 25000)
print(f"\n{o}")
print(f"Total: Rs.{o.get_total()}")
saved = o.apply_discount(10)
print(f"Discount saved: Rs.{saved}")
print(f"After discount: {o}")
print(f"As dict: {o.to_dict()}")


# ─── 3. INHERITANCE ───
# Java: public class SpecialOrder extends Order { ... }
# Python:
class SpecialOrder(OrderWithMethods):       # (parent) = extends
    def __init__(self, id, product, quantity, price, priority):
        super().__init__(id, product, quantity, price)  # Java: super()
        self.priority = priority

    def __str__(self):
        return f"[{self.priority}] {super().__str__()}"

special = SpecialOrder("ORD-003", "Server", 1, 200000, "URGENT")
print(f"\n{special}")
print(f"Total: Rs.{special.get_total()}")    # parent method works!


# ─── 4. LIST OF OBJECTS ───
# Java: List<Order> orders = new ArrayList<>();
orders = [
    OrderWithMethods("ORD-001", "Laptop", 2, 50000),
    OrderWithMethods("ORD-002", "Mouse", 10, 500),
    OrderWithMethods("ORD-003", "Monitor", 3, 25000),
    SpecialOrder("ORD-004", "Server", 1, 200000, "URGENT"),
]

print("\n--- All Orders ---")
grand_total = 0
for o in orders:
    print(f"  {o} → Total: Rs.{o.get_total()}")
    grand_total += o.get_total()
print(f"  GRAND TOTAL: Rs.{grand_total}")

# Filter expensive orders (>50000)
expensive = [o for o in orders if o.get_total() > 50000]
print(f"\nExpensive orders: {[str(o) for o in expensive]}")

# Sort by total
orders.sort(key=lambda o: o.get_total())
print(f"\nSorted by total:")
for o in orders:
    print(f"  {o}")


# ─── 5. STATIC METHOD & CLASS METHOD ───
# Java: public static Order fromDict(Map<String,Object> data)
class OrderFactory:
    order_count = 0                 # Java: static int orderCount = 0

    @staticmethod                   # Java: public static ...
    def create(product, qty, price):
        OrderFactory.order_count += 1
        id = f"ORD-{OrderFactory.order_count:03d}"
        return OrderWithMethods(id, product, qty, price)

o1 = OrderFactory.create("Laptop", 1, 50000)
o2 = OrderFactory.create("Phone", 2, 30000)
o3 = OrderFactory.create("Tablet", 1, 20000)
print(f"\nFactory orders:")
print(f"  {o1}")
print(f"  {o2}")
print(f"  {o3}")
print(f"  Total created: {OrderFactory.order_count}")


# ══════════════════════════════════════════
# SUMMARY: Java OOP vs Python OOP
# ══════════════════════════════════════════
print("\n" + "="*50)
print("JAVA OOP → PYTHON OOP")
print("="*50)
print("  class X {              → class X:")
print("  new Order()            → Order()  (no 'new')")
print("  this.id                → self.id")
print("  constructor            → __init__(self)")
print("  toString()             → __str__(self)")
print("  extends                → class Child(Parent)")
print("  super()                → super().__init__()")
print("  getters/setters        → NOT NEEDED! Direct access")
print("  public/private         → No keywords (convention: _private)")
print("  static method          → @staticmethod")
print("  implements Interface   → No interfaces (duck typing)")
print("="*50)

