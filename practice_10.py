def safe_divide(a, b):
    try:
        result = a / b
        print(f"{a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        print(f"Error: Cannot divide {a} by zero!")
        return None
    except TypeError:
        print(f"Error: Invalid types! Both must be numbers.")
        return None
    finally:
        print("Calculation done.\\n")

# Test karo
safe_divide(10, 2)       # Normal case
safe_divide(10, 0)        # Zero division
safe_divide("abc", 2)     # Type error
safe_divide(100, 3)       # Normal case