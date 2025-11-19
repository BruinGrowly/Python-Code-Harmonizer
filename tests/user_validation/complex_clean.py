class UserRepository:
    """Handles data persistence (Wisdom)."""
    def get_user(self, user_id):
        return {"id": user_id, "name": "Test"}

class UserValidator:
    """Enforces rules (Justice)."""
    def validate(self, user):
        if not user.get("name"):
            raise ValueError("Name required")
        return True

class UserService:
    """Orchestrates operations (Power/Love)."""
    def __init__(self, repo, validator):
        self.repo = repo
        self.validator = validator

    def register_user(self, user_data):
        # Love: Integration
        if self.validator.validate(user_data):
            # Power: Creation
            print(f"Registering {user_data}")
            return True
        return False
