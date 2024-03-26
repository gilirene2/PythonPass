from cryptography.fernet import Fernet
import pickle
import os.path

class PasswordManager:
    def __init__(self, key):
        self.key = key
        self.accounts = []
        self.load_accounts()

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.key)
        return cipher_suite.encrypt(data.encode())

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        return cipher_suite.decrypt(encrypted_data).decode()

    def add_account(self):
        account_name = input("Enter account name: ")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")

        encrypted_data = {
            "account_name": self.encrypt_data(account_name),
            "username": self.encrypt_data(username),
            "email": self.encrypt_data(email),
            "password": self.encrypt_data(password)
        }
        self.accounts.append(encrypted_data)
        self.save_accounts()
        print("Account added successfully.")

    def get_account(self, account_name):
        for account in self.accounts:
            if self.decrypt_data(account["account_name"]) == account_name:
                return {
                    "account_name": self.decrypt_data(account["account_name"]),
                    "username": self.decrypt_data(account["username"]),
                    "email": self.decrypt_data(account["email"]),
                    "password": self.decrypt_data(account["password"])
                }
        return "Account not found."

    def update_account(self, account_name, new_data):
        for account in self.accounts:
            if self.decrypt_data(account["account_name"]) == account_name:
                account.update(new_data)
                self.save_accounts()
                print("Account updated successfully.")
                return
        print("Account not found.")

    def delete_account(self, account_name):
        for account in self.accounts:
            if self.decrypt_data(account["account_name"]) == account_name:
                self.accounts.remove(account)
                self.save_accounts()
                print("Account deleted successfully.")
                return
        print("Account not found.")

    def list_accounts(self):
        account_list = []
        for account in self.accounts:
            account_list.append(self.decrypt_data(account["account_name"]))
        return account_list

    def save_accounts(self):
        with open("passwords.pickle", "wb") as f:
            pickle.dump(self.accounts, f)

    def load_accounts(self):
        if os.path.exists("passwords.pickle"):
            with open("passwords.pickle", "rb") as f:
                self.accounts = pickle.load(f)

if __name__ == "__main__":
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)

    password_manager = PasswordManager(key)

    while True:
        print("\nOptions:")
        print("1. Add Account")
        print("2. List Accounts")
        print("3. Retrieve Account Details")
        print("4. Update Account Details")
        print("5. Delete Account")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            password_manager.add_account()
        elif choice == "2":
            print("List of Accounts:")
            print(password_manager.list_accounts())
        elif choice == "3":
            account_name = input("Enter account name: ")
            print(password_manager.get_account(account_name))
        elif choice == "4":
            account_name = input("Enter account name: ")
            new_password = input("Enter new password: ")
            password_manager.update_account(account_name, {"password": password_manager.encrypt_data(new_password)})
        elif choice == "5":
            account_name = input("Enter account name: ")
            password_manager.delete_account(account_name)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
