my_details= {"name": "Vishawanath", "age": 34, "city": "Nainital", "skills": ["Python", "Java", "Springboot", "Microservices", "Gen AI"]}

print(f"My name is {my_details['name']}")
print(f"My first skill is {my_details['skills'][0]}")
print(f"My last skill is {my_details['skills'][-1]}")
my_details.update({"experience": 8})

print(f"My full details are {my_details}")