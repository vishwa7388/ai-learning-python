import json

class OrderManager:
    def __init__(self):
        self.orders = []

    def add_order(self, id, product, price):
        order = {"id": id, "product": product, "price": price}
        self.orders.append(order)
        print(f"Added: {id} - {product}")

    def get_total(self):
        total = 0
        for order in self.orders:
            total += order['price']
        return total

    def get_expensive(self):
        expensive = self.orders[0]
        for order in self.orders:
            if order['price'] > expensive['price']:
                expensive = order
        return expensive

    def save_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.orders, f, indent=2)
        print(f"Saved {len(self.orders)} orders to {filename}")

    def load_from_json(self, filename):
        with open(filename, "r") as f:
            self.orders = json.load(f)
        print(f"Loaded {len(self.orders)} orders from {filename}")

    def show_all(self):
        print("\\n--- All Orders ---")
        count = 0
        for order in self.orders:
            count += 1
            print(f"  {count}. {order['id']}: {order['product']} - Rs.{order['price']}")
        print(f"  Total: Rs.{self.get_total()}")


# ═══ USE KARO ═══

# Manager bana
manager = OrderManager()

# Orders add kar
manager.add_order("ORD-001", "Laptop", 50000)
manager.add_order("ORD-002", "Mouse", 500)
manager.add_order("ORD-003", "Monitor", 25000)
manager.add_order("ORD-004", "Keyboard", 1500)

# Sab dikhao
manager.show_all()

# Expensive
exp = manager.get_expensive()
print(f"\\nMost expensive: {exp['product']} (Rs.{exp['price']})")

# JSON mein save
manager.save_to_json("orders.json")

# Naya manager — JSON se load
manager2 = OrderManager()
manager2.load_from_json("orders.json")
manager2.show_all()