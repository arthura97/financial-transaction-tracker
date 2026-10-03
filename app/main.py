
from app.database.connection import get_connection

from app.repositories.user_repository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository

from app.services.user_service import UserService
from app.services.account_service import AccountService
from app.services.transaction_service import TransactionService

from decimal import Decimal

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def print_menu():
    print_header("FINANCIAL TRANSACTION TRACKER")

    print("1. Create User")
    print("2. View User")
    print("3. Create Account")
    print("4. View Account")
    print("5. Calculate Balance")
    print("6. Deposit")
    print("7. Withdraw")
    print("8. Transfer")
    print("9. View Transaction History")
    print("10. View Recent Transactions")
    print("0. Exit")

def create_user(user_service):
    print_header("CREATE USER")

    name = input("Enter name: ").strip()
    email = input("Enter email: ").strip()

    try:
        user = user_service.create_user(
            name=name,
            email=email
        )

        print("\nUser created successfully.")
        print(user)

    except ValueError as error:
        print(f"\nError: {error}")

def view_user(user_service):
    print_header("VIEW USER")

    try:
        user_id = int(input("Enter user ID: "))

        user = user_service.get_user(user_id)

        print("\nUser:")
        print(user)

    except ValueError as error:
        print(f"\nError: {error}")

def create_account(account_service):
    print_header("CREATE ACCOUNT")

    try:
        user_id = int(input("Enter user ID: "))
        account_number = input(
            "Enter account number: "
        ).strip()

        initial_balance = Decimal(
            input("Enter initial balance: ")
        )

        account = account_service.create_account(
            user_id=user_id,
            account_number=account_number,
            initial_balance=initial_balance
        )

        print("\nAccount created successfully.")
        print(account)

    except ValueError as error:
        print(f"\nError: {error}")

def view_account(account_service):
    print_header("VIEW ACCOUNT")

    try:
        account_id = int(input("Enter account ID: "))

        account = account_service.get_account(
            account_id
        )

        print("\nAccount:")
        print(account)

    except ValueError as error:
        print(f"\nError: {error}")

def calculate_balance(account_service):
    print_header("ACCOUNT BALANCE")

    try:
        account_id = int(input("Enter account ID: "))

        balance = account_service.calculate_balance(
            account_id
        )

        print(f"\nCurrent balance: {balance}")

    except ValueError as error:
        print(f"\nError: {error}")

def deposit(transaction_service):
    print_header("DEPOSIT")

    try:
        account_id = int(input("Enter account ID: "))
        amount = Decimal(
            input("Enter deposit amount: ")
        )

        account, transaction = (
            transaction_service.deposit(
                account_id=account_id,
                amount=amount
            )
        )

        print("\nDeposit successful.")

        print("\nUpdated account:")
        print(account)

        print("\nTransaction:")
        print(transaction)

    except ValueError as error:
        print(f"\nError: {error}")

def withdraw(transaction_service):
    print_header("WITHDRAW")

    try:
        account_id = int(input("Enter account ID: "))
        amount = Decimal(
            input("Enter withdrawal amount: ")
        )

        account, transaction = (
            transaction_service.withdraw(
                account_id=account_id,
                amount=amount
            )
        )

        print("\nWithdrawal successful.")

        print("\nUpdated account:")
        print(account)

        print("\nTransaction:")
        print(transaction)

    except ValueError as error:
        print(f"\nError: {error}")

def transfer(transaction_service):
    print_header("TRANSFER")

    try:
        source_account_id = int(
            input("Enter source account ID: ")
        )

        destination_account_id = int(
            input("Enter destination account ID: ")
        )

        amount = Decimal(
            input("Enter transfer amount: ")
        )

        (
            source_account,
            destination_account,
            outgoing_transaction,
            incoming_transaction
        ) = transaction_service.transfer(
            source_account_id=source_account_id,
            destination_account_id=destination_account_id,
            amount=amount
        )

        print("\nTransfer successful.")

        print("\nSource account:")
        print(source_account)

        print("\nDestination account:")
        print(destination_account)

        print("\nTRANSFER_OUT:")
        print(outgoing_transaction)

        print("\nTRANSFER_IN:")
        print(incoming_transaction)

    except ValueError as error:
        print(f"\nError: {error}")

def view_transaction_history(transaction_service):
    print_header("TRANSACTION HISTORY")

    try:
        account_id = int(input("Enter account ID: "))

        transactions = (
            transaction_service
            .view_transaction_history(account_id)
        )

        if not transactions:
            print("\nNo transactions found.")
            return

        print()

        for transaction in transactions:
            print(transaction)

    except ValueError as error:
        print(f"\nError: {error}")

def view_recent_transactions(transaction_service):
    print_header("RECENT TRANSACTIONS")

    try:
        account_id = int(input("Enter account ID: "))

        limit = int(
            input(
                "How many transactions do you want to see? "
            )
        )

        transactions = (
            transaction_service
            .view_recent_transactions(
                account_id=account_id,
                limit=limit
            )
        )

        if not transactions:
            print("\nNo transactions found.")
            return

        print()

        for transaction in transactions:
            print(transaction)

    except ValueError as error:
        print(f"\nError: {error}")


def main():

    with get_connection() as connection:

        # Repositories
        user_repository = UserRepository(
            connection
        )

        account_repository = AccountRepository(
            connection
        )

        transaction_repository = TransactionRepository(
            connection
        )

        # Services
        user_service = UserService(
            user_repository
        )

        account_service = AccountService(
            account_repository,
            user_repository
        )

        transaction_service = TransactionService(
            transaction_repository,
            account_repository
        )

        # Main CLI Loop
        while True:

            print_menu()

            choice = input(
                "\nSelect an option: "
            ).strip()

            if choice == "1":
                create_user(user_service)

            elif choice == "2":
                view_user(user_service)

            elif choice == "3":
                create_account(account_service)

            elif choice == "4":
                view_account(account_service)

            elif choice == "5":
                calculate_balance(account_service)

            elif choice == "6":
                deposit(transaction_service)

            elif choice == "7":
                withdraw(transaction_service)

            elif choice == "8":
                transfer(transaction_service)

            elif choice == "9":
                view_transaction_history(
                    transaction_service
                )

            elif choice == "10":
                view_recent_transactions(
                    transaction_service
                )

            elif choice == "0":
                print("\nGoodbye!")
                break

            else:
                print(
                    "\nInvalid option. "
                    "Please select a valid menu item."
                )

if __name__ == "__main__":
    main()


