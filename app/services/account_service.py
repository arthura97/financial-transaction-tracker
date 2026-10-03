
class AccountService:

    def __init__(
        self,
        account_repository,
        user_repository
    ):
        self.account_repository = account_repository
        self.user_repository = user_repository

    def create_account(
        self,
        user_id,
        account_number,
        initial_balance=0
    ):
        if initial_balance < 0:
            raise ValueError(
                "Initial balance cannot be negative."
            )

        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        existing_account = (
            self.account_repository
            .get_account_by_number(account_number)
        )

        if existing_account is not None:
            raise ValueError(
                "An account with this number already exists."
            )

        try:
            account = self.account_repository.create_account(
                user_id=user_id,
                account_number=account_number,
                balance=initial_balance
            )

            self.account_repository.connection.commit()

            return account

        except Exception:
            self.account_repository.connection.rollback()
            raise

    def get_account(self, account_id):
        account = (
            self.account_repository
            .get_account_by_id(account_id)
        )

        if account is None:
            raise ValueError("Account not found.")

        return account

    def calculate_balance(self, account_id):
        account = self.get_account(account_id)

        return account.balance


