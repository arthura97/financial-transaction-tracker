
from app.model.user import User

class UserRepository:

    def __init__(self, connection):
        self.connection = connection

    def create_user(self, name, email):
        query = """
            INSERT INTO users (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email, created_at;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (name, email))
            row = cursor.fetchone()

        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            created_at=row[3]
        )

    def get_user_by_id(self, user_id):
        query = """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()

        if row is None:
            return None

        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            created_at=row[3]
        )

    def get_user_by_email(self, email):
        query = """
            SELECT id, name, email, created_at
            FROM users
            WHERE email = %s;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

        if row is None:
            return None

        return User(
            id=row[0],
            name=row[1],
            email=row[2],
            created_at=row[3]
        )


