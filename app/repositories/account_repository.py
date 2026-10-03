
from app.model.account import Account

class AccountRepository:

    def __init__(self, connection):
        self.connection = connection

    def create_account(
        self,
        user_id,
        account_number,
        balance=0
    ):
        query = """
            INSERT INTO accounts (
                user_id,
                account_number,
                balance
            )
            VALUES (%s, %s, %s)
            RETURNING
                id,
                user_id,
                account_number,
                balance,
                created_at;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (user_id, account_number, balance)
            )

            row = cursor.fetchone()

        return Account(
            id=row[0],
            user_id=row[1],
            account_number=row[2],
            balance=row[3],
            created_at=row[4]
        )

    def get_account_by_id(self, account_id):
        query = """
            SELECT
                id,
                user_id,
                account_number,
                balance,
                created_at
            FROM accounts
            WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (account_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Account(
            id=row[0],
            user_id=row[1],
            account_number=row[2],
            balance=row[3],
            created_at=row[4]
        )

    def get_account_by_number(self, account_number):
        query = """
            SELECT
                id,
                user_id,
                account_number,
                balance,
                created_at
            FROM accounts
            WHERE account_number = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (account_number,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Account(
            id=row[0],
            user_id=row[1],
            account_number=row[2],
            balance=row[3],
            created_at=row[4]
        )

    def get_accounts_by_user_id(self, user_id):
        query = """
            SELECT
                id,
                user_id,
                account_number,
                balance,
                created_at
            FROM accounts
            WHERE user_id = %s
            ORDER BY id;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

        return [
            Account(
                id=row[0],
                user_id=row[1],
                account_number=row[2],
                balance=row[3],
                created_at=row[4]
            )
            for row in rows
        ]

    def update_balance(self, account_id, new_balance):
        query = """
            UPDATE accounts
            SET balance = %s
            WHERE id = %s
            RETURNING
                id,
                user_id,
                account_number,
                balance,
                created_at;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                (new_balance, account_id)
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return Account(
            id=row[0],
            user_id=row[1],
            account_number=row[2],
            balance=row[3],
            created_at=row[4]
        )

    def get_account_for_update(self, account_id):
        """
        Lock the account row during a financial operation.
        """

        query = """
            SELECT
                id,
                user_id,
                account_number,
                balance,
                created_at
            FROM accounts
            WHERE id = %s
            FOR UPDATE;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (account_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return Account(
            id=row[0],
            user_id=row[1],
            account_number=row[2],
            balance=row[3],
            created_at=row[4]
        )



