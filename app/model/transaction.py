
class Transaction:
    def __init__(self, id, account_id, transaction_type, amount, created_at):
        self.id = id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.created_at = created_at

    def __repr__(self):
        return (
            f"Transaction("
            f"id={self.id}, "
            f"account_id={self.account_id}, "
            f"transaction_type='{self.transaction_type}', "
            f"amount={self.amount}, "
            f"created_at={self.created_at}"
            f")"
        )


