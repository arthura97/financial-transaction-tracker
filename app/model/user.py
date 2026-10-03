
class User:
    def __init__(self, id, name, email, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at

    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"email='{self.email}', "
            f"created_at={self.created_at}"
            f")"
        )


