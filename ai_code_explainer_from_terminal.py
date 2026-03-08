import requests

def ask_ai(question):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": question,
                "stream": False
            },
            timeout=120
        )
        data = response.json()
        return data.get('response', 'No response key found')
    except Exception as e:
        return f"Error: {e}"

java_code = """
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
}
"""

print("=== AI Code Analyzer ===")
print("Java code loaded! Puch kuch bhi...")
print("Type 'quit' to exit\n")

while True:
    question = input("Tera sawaal: ")
    if question.lower() == 'quit':
        print("Bye!")
        break
    prompt = f"{question}\n\nCode:\n{java_code}"
    print("\nAI soch raha hai...\n")
    answer = ask_ai(prompt)
    print(f"AI: {answer}\n")
    print("-" * 50)