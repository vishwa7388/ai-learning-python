
def format_price(amount):
    return f"Rs.{amount:,.2f}"

def generate_id(prefix, number):
    return f"{prefix}-{number:03d}"

ORDER_STATUS = ["PENDING", "CONFIRMED", "SHIPPED", "DELIVERED"]
