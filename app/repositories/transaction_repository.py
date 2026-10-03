
from app.model.transaction import Transaction

class TransactionRepository:

    def __init__(self, connection):
        self.connection = connection

    def create_transaction(
        self,
        account_id,
        transaction_type,
        amount
    ):
        query = """
            INSERT INTO transactions (
                account_id,
                transaction_type,
                amount
            )
            VALUES (%s, %s, %s)
            RETURNING
                id,
                account_id,
                transaction_type,
                amount,
                created_at;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    account_id,
                    transaction_type,
                    amount
                )
            )

            row = cursor.fetchone()

        return Transaction(
            id=row[0],
            account_id=row[1],
            transaction_type=row[2],
            amount=row[3],
            created_at=row[4]
        )

    def get_transaction_by_id(self, transaction_id):
        query = """
            SELECT
                id,
                account_id,
                transaction_type,
                amount,
                created_at
            FROM transactions
            WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (transaction_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Transaction(
            id=row[0],
            account_id=row[1],
            transaction_type=row[2],
            amount=row[3],
            created_at=row[4]
        )

    def get_transactions_by_account_id(self, account_id):
        query = """
            SELECT
                id,
                account_id,
                transaction_type,
                amount,
                created_at
            FROM transactions
            WHERE account_id = %s
            ORDER BY created_at DESC, id DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (account_id,))
            rows = cursor.fetchall()

        return [
            Transaction(
                id=row[0],
                account_id=row[1],
                transaction_type=row[2],
                amount=row[3],
                created_at=row[4]
            )
            for row in rows
        ]

    def get_recent_transactions(self, account_id, limit=10):
        query = """
            SELECT
                id,
                account_id,
                transaction_type,
                amount,
                created_at
            FROM transactions
            WHERE account_id = %s
            ORDER BY created_at DESC, id DESC
            LIMIT %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (account_id, limit)
            )

            rows = cursor.fetchall()

        return [
            Transaction(
                id=row[0],
                account_id=row[1],
                transaction_type=row[2],
                amount=row[3],
                created_at=row[4]
            )
            for row in rows
        ]



