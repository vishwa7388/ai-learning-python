def calculate_salary(basic, bonus, tax_percent):
    total = basic + bonus
    tax = total * tax_percent / 100
    in_hand = total - tax
    return in_hand


print(f"The Salary is {calculate_salary(100000, 10000, 10)}")