# simple_calculator.py

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b


def calculate(a, b, operator):
    if operator == "+":
        return add(a, b)
    elif operator == "-":
        return subtract(a, b)
    elif operator == "*":
        return multiply(a, b)
    elif operator == "/":
        return divide(a, b)
    else:
        return "Invalid operator"


def show_menu():
    print("\n--- Simple Calculator ---")
    print("1. Perform Calculation")
    print("2. Clear")
    print("3. Exit")


def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            try:
                num1 = float(input("Enter first number: "))
                operator = input("Enter operator (+, -, *, /): ")
                num2 = float(input("Enter second number: "))

                result = calculate(num1, num2, operator)
                print("Result:", result)

            except ValueError:
                print("Invalid input! Please enter numbers only.")

        elif choice == "2":
            print("Calculator cleared!")

        elif choice == "3":
            print("Exiting calculator. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__"