
class Account:
    def __init__(self, id, user_id, account_number, balance, created_at):
        self.id = id
        self.user_id = user_id
        self.account_number = account_number
        self.balance = balance
        self.created_at = created_at

    def __repr__(self):
        return (
            f"Account("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"account_number='{self.account_number}', "
            f"balance={self.balance}, "
            f"created_at={self.created_at}"
            f")"
        )



