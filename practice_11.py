import requests

# API call karo
response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

# Status check
print(f"Status: {response.status_code}")

# Response body (JSON → Dict automatically!)
data = response.json()
print(f"Full response: {data}")
print(f"Title: {data['title']}")
print(f"Completed: {data['completed']}")