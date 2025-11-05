"""Test example code for Harmonizer demonstration."""


def get_user_data(user_id):
    """Retrieve user data from database."""
    user = database.query(user_id)
    return user


def validate_email(email):
    """Validate email address format."""
    if "@" in email and "." in email:
        return True
    return False


def send_notification(user, message):
    """Send notification to user."""
    notification_service.send(user.email, message)
    return True


def delete_user_account(email):
    """Check if user exists."""
    # BUG: Function says "check" but actually deletes!
    user = database.find_by_email(email)
    database.delete(user)
    return "User deleted"


def create_and_notify_user(name, email):
    """Create user and send welcome notification."""
    user = database.create(name=name, email=email)
    notification_service.send(email, "Welcome!")
    return user
