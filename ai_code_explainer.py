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
}
"""

prompt = f"Explain this Java code in 3 lines:\n{java_code}"

print("Asking AI...")
answer = ask_ai(prompt)
print(f"AI says:\n{answer}")