class Employee:
    def __init__(self, name, role, salary):
        self.name = name
        self.role = role
        self.salary = salary

    def get_annual_salary(self):
        return self.salary * 12

    def promote(self):
        self.salary = self.salary * 1.2
        print(f"{self.name} promoted! New salary: Rs.{self.salary}")

    def __str__(self):
        return f"{self.name} ({self.role}) - Rs.{self.salary}/month"


class AIEngineer(Employee):
    def __init__(self, name, salary, skills):
        super().__init__(name, "AI Engineer", salary)
        self.skills = skills

    def show_skills(self):
        print(f"{self.name}'s skills:")
        for skill in self.skills:
            print(f"  - {skill}")

    def __str__(self):
        skills_str = ", ".join(self.skills)
        return f"{self.name} ({self.role}) - Rs.{self.salary} | Skills: {skills_str}"

# Object bana
ai_dev = AIEngineer("Vishawanath", 150000, ["Java", "Spring Boot", "Python", "LangChain", "RAG"])
print(ai_dev)
ai_dev.show_skills()
ai_dev.promote()
print(ai_dev)
