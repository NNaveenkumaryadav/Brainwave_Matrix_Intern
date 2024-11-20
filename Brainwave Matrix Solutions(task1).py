import json

class ATM:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.load_users()
        self.current_user = None

    def load_users(self):
        try:
            with open(self.users_file, 'r') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        with open(self.users_file, 'w') as file:
            json.dump(self.users, file, indent=4)

    def authenticate_user(self):
        pin = input("Enter PIN: ")

        for user_id, user in self.users.items():
            if user['pin'] == pin:
                self.current_user = user_id
                print("Login successful!")
                return
        print("Invalid PIN.")

    def display_menu(self):
        print("\n==== ATM Menu ====")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Change PIN")
        print("6. Display Mobile Number")
        print("7. Change Mobile Number")
        print("8. Exit")
        print("===================")

    def check_balance(self):
        balance = self.users[self.current_user]['balance']
        print(f"Your current balance is: ${balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self.users[self.current_user]['balance'] += amount
            self.users[self.current_user]['transactions'].append(f"Deposited ${amount:.2f}")
            print(f"Successfully deposited ${amount:.2f}")
            self.save_users()
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.users[self.current_user]['balance']:
                self.users[self.current_user]['balance'] -= amount
                self.users[self.current_user]['transactions'].append(f"Withdrew ${amount:.2f}")
                print(f"Successfully withdrew ${amount:.2f}")
                self.save_users()
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def show_transaction_history(self):
        transactions = self.users[self.current_user]['transactions']
        if transactions:
            print("\nTransaction History:")
            for transaction in transactions:
                print(transaction)
        else:
            print("No transactions found.")

    def change_pin(self):
        current_pin = input("Enter current PIN: ")
        if current_pin == self.users[self.current_user]['pin']:
            new_pin = input("Enter new PIN: ")
            confirm_pin = input("Confirm new PIN: ")
            if new_pin == confirm_pin:
                self.users[self.current_user]['pin'] = new_pin
                print("PIN changed successfully.")
                self.save_users()
            else:
                print("PINs do not match.")
        else:
            print("Incorrect current PIN.")

    def display_mobile_number(self):
        mobile_number = self.users[self.current_user]['mobile_number']
        print(f"Your registered mobile number is: {mobile_number}")

    def change_mobile_number(self):
        new_mobile_number = input("Enter new mobile number: ")
        confirm_mobile_number = input("Confirm new mobile number: ")
        if new_mobile_number == confirm_mobile_number:
            self.users[self.current_user]['mobile_number'] = new_mobile_number
            print("Mobile number changed successfully.")
            self.save_users()
        else:
            print("Mobile numbers do not match.")

    def run(self):
        while True:
            self.authenticate_user()
            if self.current_user:
                break

        while True:
            self.display_menu()
            choice = input("Please choose an option: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                amount = float(input("Enter deposit amount: "))
                self.deposit(amount)
            elif choice == '3':
                amount = float(input("Enter withdrawal amount: "))
                self.withdraw(amount)
            elif choice == '4':
                self.show_transaction_history()
            elif choice == '5':
                self.change_pin()
            elif choice == '6':
                self.display_mobile_number()
            elif choice == '7':
                self.change_mobile_number()
            elif choice == '8':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
            print("\n")

if __name__ == "__main__":
    initial_users = {
        "user1": {
            "pin": "1234",
            "balance": 100.0,
            "transactions": [],
            "mobile_number": "123-456-7890"
        },
        "user2": {
            "pin": "5678",
            "balance": 200.0,
            "transactions": [],
            "mobile_number": "098-765-4321"
        }
    }
    
    with open('users.json', 'w') as file:
        json.dump(initial_users, file, indent=4)
    
    atm = ATM()
    atm.run()
