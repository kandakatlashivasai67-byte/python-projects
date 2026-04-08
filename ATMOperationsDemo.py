from ATMMenu import Menu
from ATMOperations import *
from ATMExcept import DepositError, WithdrawError, InSuffFundError

customers = {}

while True:
    try:
        Menu()
        ch = int(input("Enter your choice: "))

        match ch:
            case 1:
                acc = input("Enter Account Number: ")
                pin = input("Enter PIN: ")

                if acc in customers and customers[acc]["pin"] == pin:
                    try:
                        deposit(customers[acc])
                    except DepositError:
                        print("\tInvalid deposit amount")
                else:
                    print("\tInvalid Account or PIN")

            case 2:
                acc = input("Enter Account Number: ")
                pin = input("Enter PIN: ")

                if acc in customers and customers[acc]["pin"] == pin:
                    try:
                        withdraw(customers[acc])
                    except WithdrawError:
                        print("\tInvalid withdraw amount")
                    except InSuffFundError:
                        print("\tInsufficient balance")
                else:
                    print("\tInvalid Account or PIN")

            case 3:
                acc = input("Enter Account Number: ")
                pin = input("Enter PIN: ")

                if acc in customers and customers[acc]["pin"] == pin:
                    balenq(customers[acc])
                else:
                    print("\tInvalid Account or PIN")

            case 4:
                create_customer(customers)

            case 5:
                view_customer(customers)

            case 6:
                view_all_customers(customers)

            case 7:
                update_customer(customers)

            case 8:
                delete_customer(customers)

            case 9:
                print("Thank you for using ATM!")
                break

            case _:
                print("\tInvalid choice")

    except ValueError:
        print("\tEnter valid number only")