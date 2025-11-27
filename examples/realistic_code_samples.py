"""
Realistic Code Samples for Testing Enhanced Parser
Demonstrates real-world functions with proper LJPW semantic mapping.
"""

from datetime import datetime

# ============================================================================
# HARMONIOUS FUNCTIONS (Intent matches Execution)
# ============================================================================


def get_user_by_id(user_id):
    """
    Retrieve user information from database.
    INTENT: WISDOM (get = information retrieval)
    EXECUTION: WISDOM (query + return = information operations)
    Expected harmony: EXCELLENT (~0.05)
    """
    user_data = database.query(f"SELECT * FROM users WHERE id = {user_id}")
    return user_data


def validate_email_format(email):
    """
    Validate email address format.
    INTENT: JUSTICE (validate = correctness checking)
    EXECUTION: JUSTICE (if/else = logical structure)
    Expected harmony: EXCELLENT (~0.05)
    """
    if "@" not in email or "." not in email:
        return False
    return True


def create_user_account(username, email):
    """
    Create new user account in database.
    INTENT: POWER (create = state transformation)
    EXECUTION: POWER (assignments, database.save = modifications)
    Expected harmony: EXCELLENT (~0.05)
    """
    user = User()
    user.username = username
    user.email = email
    database.users.save(user)
    return user


def send_welcome_email(user_email):
    """
    Send welcome email to new user.
    INTENT: LOVE (send = communication)
    EXECUTION: LOVE (email.send = communication operation)
    Expected harmony: EXCELLENT (~0.05)
    """
    message = "Welcome to our platform!"
    email_service.send(to=user_email, body=message)


# ============================================================================
# DISHARMONIOUS FUNCTIONS (Intent contradicts Execution)
# ============================================================================


def check_user_permissions(user_token):
    """
    Check user permissions.
    INTENT: JUSTICE (check = validation)
    EXECUTION: POWER (database.delete = destructive action)
    Expected harmony: CRITICAL DISHARMONY (~1.2)
    THIS IS A BUG - Function says it "checks" but actually "deletes"!
    """
    # BUG: This deletes the user instead of checking permissions!
    database.delete_user(user_token)
    return "Deleted"


def get_cached_data(cache_key):
    """
    Get data from cache.
    INTENT: WISDOM (get = information retrieval)
    EXECUTION: POWER (del = destruction) + WISDOM (return)
    Expected harmony: MEDIUM DISHARMONY (~0.6)
    THIS IS A BUG - Should "get" but also "pops" (destructive read)!
    """
    value = cache[cache_key]
    del cache[cache_key]  # BUG: Also removes from cache (destructive)!
    return value


def validate_and_save_user(user_data):
    """
    Validate user data.
    INTENT: JUSTICE (validate = validation)
    EXECUTION: POWER (database.save = modification)
    Expected harmony: MEDIUM DISHARMONY (~0.7)
    Function name says "validate" but actually does BOTH validate AND save.
    """
    if not user_data.get("email"):
        raise ValueError("Email required")

    # The name says ONLY "validate" but it also saves!
    user = User(user_data)
    database.users.save(user)
    return user.id


def calculate_and_notify(items):
    """
    Calculate total.
    INTENT: WISDOM (calculate = computation)
    EXECUTION: WISDOM (sum) + LOVE (notify = communication)
    Expected harmony: MEDIUM DISHARMONY (~0.5)
    Function name says "calculate" but also sends notifications.
    """
    total = sum(item.price for item in items)

    # This notification isn't mentioned in the function name!
    notify_admin(f"Total calculated: {total}")

    return total


# ============================================================================
# COMPLEX MIXED FUNCTIONS (Multiple dimensions, properly named)
# ============================================================================


def fetch_validate_and_save_user(user_id, updates):
    """
    Fetch user, validate updates, and save changes.
    INTENT: WISDOM (fetch) + JUSTICE (validate) + POWER (save)
    EXECUTION: All three dimensions present
    Expected harmony: GOOD (~0.15)
    Function name accurately describes all operations.
    """
    # WISDOM: Fetch user data
    user = database.get_user(user_id)

    # JUSTICE: Validate updates
    if not updates.get("email"):
        raise ValueError("Email required")

    # POWER: Apply updates and save
    user.email = updates["email"]
    database.save_user(user)

    return user


def process_order_with_notification(order_id):
    """
    Process order and notify customer.
    INTENT: POWER (process) + LOVE (notification)
    EXECUTION: POWER + LOVE dimensions present
    Expected harmony: GOOD (~0.15)
    Function name mentions both processing and notification.
    """
    # POWER: Process the order
    order = database.get_order(order_id)
    order.status = "processed"
    database.save_order(order)

    # LOVE: Notify customer
    send_email(order.customer_email, "Order processed!")

    return order


# ============================================================================
# DIMENSION-SPECIFIC EXAMPLES
# ============================================================================


# Pure WISDOM functions
def calculate_total_price(items):
    """Pure computation - returns information."""
    return sum(item.price for item in items)


def analyze_sales_data(sales_records):
    """Pure analysis - derives insights from data."""
    total_sales = sum(r.amount for r in sales_records)
    average_sale = total_sales / len(sales_records)
    return {"total": total_sales, "average": average_sale}


# Pure JUSTICE functions
def verify_authentication_token(token):
    """Pure validation - checks correctness."""
    if not token:
        return False
    if token.expired():
        return False
    return token.is_valid()


def filter_active_users(users):
    """Pure filtering - applies logical criteria."""
    return [u for u in users if u.active and not u.banned]


# Pure POWER functions
def initialize_database_connection():
    """Pure execution - performs action."""
    conn = Database()
    conn.connect()
    return conn


def delete_expired_sessions():
    """Pure destruction - removes data."""
    expired = database.query("SELECT * FROM sessions WHERE expired = true")
    for session in expired:
        database.delete_session(session.id)


# Pure LOVE functions
def broadcast_system_message(message):
    """Pure communication - sends to all users."""
    for user in get_all_users():
        send_notification(user, message)


def merge_user_profiles(profile1, profile2):
    """Pure integration - combines data."""
    return {**profile1, **profile2, "merged_at": datetime.now()}


# ============================================================================
# Mock objects for testing
# ============================================================================


class Database:
    def query(self, sql):
        return {"id": 1, "name": "Test User"}

    def get_user(self, user_id):
        return User()

    def save_user(self, user):
        pass

    def delete_user(self, token):
        pass

    def get_order(self, order_id):
        return Order()

    def save_order(self, order):
        pass


class User:
    def __init__(self, data=None):
        self.username = ""
        self.email = ""
        self.active = True
        self.banned = False

    def expired(self):
        return False

    def is_valid(self):
        return True


class Order:
    def __init__(self):
        self.status = "pending"
        self.customer_email = "test@example.com"


database = Database()
cache = {}
email_service = None


def send_email(to, body):
    pass


def send_notification(user, message):
    pass


def notify_admin(message):
    pass


def get_all_users():
    return []
