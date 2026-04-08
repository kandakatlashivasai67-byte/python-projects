from ATMExcept import DepositError, WithdrawError, InSuffFundError

def deposit(customer):
    damt = float(input("Enter Deposit Amount: "))
    if damt <= 0:
        raise DepositError("Invalid deposit amount")

    customer["bal"] += damt
    print(f"\tAccount {customer['name']} credited with INR {damt}")
    print(f"\tBalance after Deposit: INR {customer['bal']}")


def withdraw(customer):
    wamt = float(input("Enter Withdraw Amount: "))
    if wamt <= 0:
        raise WithdrawError("Invalid withdraw amount")

    if wamt > customer["bal"]:
        raise InSuffFundError("Insufficient balance")

    customer["bal"] -= wamt
    print(f"\tAccount {customer['name']} debited with INR {wamt}")
    print(f"\tBalance after Withdraw: INR {customer['bal']}")


def balenq(customer):
    print(f"\tAccount {customer['name']} balance: INR {customer['bal']}")


def create_customer(customers):
    acc_no = input("Enter Account Number: ")

    if acc_no in customers:
        print("\tAccount already exists")
        return

    name = input("Enter Name: ")
    bal = float(input("Enter Initial Balance: "))
    pin = input("Set 4-digit PIN: ")

    customers[acc_no] = {"name": name, "bal": bal, "pin": pin}
    print(f"\tCustomer {name} created successfully!")


def view_customer(customers):
    acc_no = input("Enter Account Number: ")

    if acc_no in customers:
        c = customers[acc_no]
        print(f"\tName: {c['name']}, Balance: {c['bal']}, PIN: {c['pin']}")
    else:
        print("\tCustomer not found!")


def view_all_customers(customers):
    if not customers:
        print("\tNo customers available")
        return

    for acc, c in customers.items():
        print(f"\tAcc: {acc}, Name: {c['name']}, Balance: {c['bal']}, PIN: {c['pin']}")


def update_customer(customers):
    acc_no = input("Enter Account Number: ")

    if acc_no in customers:
        c = customers[acc_no]

        name = input(f"Enter new name [{c['name']}]: ") or c["name"]
        bal_input = input(f"Enter new balance [{c['bal']}]: ")
        bal = float(bal_input) if bal_input else c["bal"]
        pin = input(f"Enter new PIN [{c['pin']}]: ") or c["pin"]

        c["name"] = name
        c["bal"] = bal
        c["pin"] = pin

        print("\tCustomer updated successfully!")
    else:
        print("\tCustomer not found!")


def delete_customer(customers):
    acc_no = input("Enter Account Number: ")

    if acc_no in customers:
        del customers[acc_no]
        print("\tCustomer deleted successfully!")
    else:
        print("\tCustomer not found!")