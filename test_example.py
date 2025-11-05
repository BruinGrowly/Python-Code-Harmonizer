"""Test example code for Harmonizer demonstration."""

# Mock services for demonstration purposes
database = None  # noqa: F811 - Mock database service
notification_service = None  # noqa: F811 - Mock notification service


def get_user_data(user_id):
    """Retrieve user data from database."""
    user = database.query(user_id)  # noqa: F821
    return user


def validate_email(email):
    """Validate email address format."""
    if "@" in email and "." in email:
        return True
    return False


def send_notification(user, message):
    """Send notification to user."""
    notification_service.send(user.email, message)  # noqa: F821
    return True


def delete_user_account(email):
    """Check if user exists."""
    # BUG: Function says "check" but actually deletes!
    user = database.find_by_email(email)  # noqa: F821
    database.delete(user)  # noqa: F821
    return "User deleted"


def create_and_notify_user(name, email):
    """Create user and send welcome notification."""
    user = database.create(name=name, email=email)  # noqa: F821
    notification_service.send(email, "Welcome!")  # noqa: F821
    return user
