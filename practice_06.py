class Employee:
    def __init__(self,name, role, salary):
        self.name = name
        self.role = role
        self.salary = salary

    def get_annual_salary(self):
        return self.salary * 12

    def promote(self, percentage):
        self.salary = self.salary * 1.2
        return f"Employee got a increment of 20% and new salary is Rs.{self.salary}/month"

    def __str__(self):
        return f"Employee(name={self.name}, role={self.role} -- salary=Rs.{self.salary}/month)"

emp = Employee("Vishwanath", "Software Engineer", 100000)
print(f"Annual salary: {emp.get_annual_salary()}")
print(emp)
print(emp.promote(20))
print(f"final salary: {emp.salary}")