
class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, name, email):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")

        if not email or not email.strip():
            raise ValueError("Email cannot be empty.")

        name = name.strip()
        email = email.strip()

        existing_user = (
            self.user_repository
            .get_user_by_email(email)
        )

        if existing_user is not None:
            raise ValueError(
                "A user with this email already exists."
            )

        try:
            user = self.user_repository.create_user(
                name=name,
                email=email
            )

            self.user_repository.connection.commit()

            return user

        except Exception:
            self.user_repository.connection.rollback()
            raise

    def get_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        return user


