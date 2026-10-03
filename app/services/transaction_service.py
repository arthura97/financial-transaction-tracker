
from decimal import Decimal

class TransactionService:

    def __init__(
        self,
        transaction_repository,
        account_repository
    ):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    # Deposit
    def deposit(self, account_id, amount):
        amount = self._validate_amount(amount)

        try:
            # Lock account row
            account = (
                self.account_repository
                .get_account_for_update(account_id)
            )

            if account is None:
                raise ValueError("Account not found.")

            # Calculate new balance
            new_balance = account.balance + amount

            # Update account balance
            updated_account = (
                self.account_repository
                .update_balance(
                    account_id,
                    new_balance
                )
            )

            # Create transaction record
            transaction = (
                self.transaction_repository
                .create_transaction(
                    account_id=account_id,
                    transaction_type="DEPOSIT",
                    amount=amount
                )
            )

            # Commit both operations
            self.transaction_repository.connection.commit()

            return updated_account, transaction

        except Exception:
            self.transaction_repository.connection.rollback()
            raise

    # Withdraw
    def withdraw(self, account_id, amount):
        amount = self._validate_amount(amount)

        try:
            # Lock account row
            account = (
                self.account_repository
                .get_account_for_update(account_id)
            )

            if account is None:
                raise ValueError("Account not found.")

            # Check available balance
            if account.balance < amount:
                raise ValueError("Insufficient funds.")

            # Calculate new balance
            new_balance = account.balance - amount

            # Update account balance
            updated_account = (
                self.account_repository
                .update_balance(
                    account_id,
                    new_balance
                )
            )

            # Create transaction record
            transaction = (
                self.transaction_repository
                .create_transaction(
                    account_id=account_id,
                    transaction_type="WITHDRAWAL",
                    amount=amount
                )
            )

            # Commit both operations
            self.transaction_repository.connection.commit()

            return updated_account, transaction

        except Exception:
            self.transaction_repository.connection.rollback()
            raise

    # Transfer
    def transfer(
        self,
        source_account_id,
        destination_account_id,
        amount
    ):
        amount = self._validate_amount(amount)

        # Source and destination cannot be the same
        if source_account_id == destination_account_id:
            raise ValueError(
                "Source and destination accounts must be different."
            )

        try:
            # Lock accounts in deterministic order
            # Always lock the account with the smaller ID first.
            # This helps prevent deadlocks when multiple
            # transfers happen at the same time.

            first_account_id = min(
                source_account_id,
                destination_account_id
            )

            second_account_id = max(
                source_account_id,
                destination_account_id
            )

            first_account = (
                self.account_repository
                .get_account_for_update(
                    first_account_id
                )
            )

            if first_account is None:
                raise ValueError(
                    "First account not found."
                )

            second_account = (
                self.account_repository
                .get_account_for_update(
                    second_account_id
                )
            )

            if second_account is None:
                raise ValueError(
                    "Second account not found."
                )

            # Identify source and destination
            if source_account_id == first_account_id:
                source_account = first_account
                destination_account = second_account
            else:
                source_account = second_account
                destination_account = first_account

            # Check source balance
            if source_account.balance < amount:
                raise ValueError(
                    "Insufficient funds."
                )

            # Calculate new balances
            source_new_balance = (
                source_account.balance - amount
            )

            destination_new_balance = (
                destination_account.balance + amount
            )

            # Update source account
            updated_source = (
                self.account_repository
                .update_balance(
                    source_account_id,
                    source_new_balance
                )
            )

            # Update destination account
            updated_destination = (
                self.account_repository
                .update_balance(
                    destination_account_id,
                    destination_new_balance
                )
            )

            # Create TRANSFER_OUT transaction
            outgoing_transaction = (
                self.transaction_repository
                .create_transaction(
                    account_id=source_account_id,
                    transaction_type="TRANSFER_OUT",
                    amount=amount
                )
            )

            # Create TRANSFER_IN transaction
            incoming_transaction = (
                self.transaction_repository
                .create_transaction(
                    account_id=destination_account_id,
                    transaction_type="TRANSFER_IN",
                    amount=amount
                )
            )

            # Commit everything atomically
            self.transaction_repository.connection.commit()

            return (
                updated_source,
                updated_destination,
                outgoing_transaction,
                incoming_transaction
            )

        except Exception:
            # If ANY operation fails, undo ALL changes in this transaction.
            self.transaction_repository.connection.rollback()
            raise

    # View Transaction History
    def view_transaction_history(self, account_id):
        account = (
            self.account_repository
            .get_account_by_id(account_id)
        )

        if account is None:
            raise ValueError("Account not found.")

        return (
            self.transaction_repository
            .get_transactions_by_account_id(account_id)
        )

    # View Recent Transactions
    def view_recent_transactions(
        self,
        account_id,
        limit=10
    ):
        account = (
            self.account_repository
            .get_account_by_id(account_id)
        )

        if account is None:
            raise ValueError("Account not found.")

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than zero."
            )

        return (
            self.transaction_repository
            .get_recent_transactions(
                account_id,
                limit
            )
        )

    # Private Helper
    @staticmethod
    def _validate_amount(amount):
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError(
                "Amount must be greater than zero."
            )

        return amount



