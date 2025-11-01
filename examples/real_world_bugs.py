"""
Real-World Semantic Bugs Caught by Python Code Harmonizer

This file demonstrates ACTUAL semantic bugs that Harmonizer catches,
but other tools (Pylint, MyPy, Pytest) might miss.

Each example shows:
1. The buggy code
2. What Harmonizer reports
3. Why it's a problem
4. The fix

Run: harmonizer examples/real_world_bugs.py
"""

# =============================================================================
# BUG #1: Validation Function That Modifies
# =============================================================================
# HARMONIZER SCORE: ~0.85 (!! DISHARMONY)
# OTHER TOOLS: All pass ✓


def validate_email(email: str) -> bool:
    """
    BUG: Function claims to validate, but actually sends emails!

    Harmonizer catches:
    - "validate" = Wisdom (checking/reading)
    - "send" = Power (action/writing)
    - High semantic distance = DISHARMONY

    Other tools miss this because:
    - Pylint: No style violation
    - MyPy: Types are correct (str -> bool)
    - Pytest: If test expects True, it passes
    """
    if "@" in email and "." in email:
        # VIOLATION: Validation function shouldn't send emails!
        send_welcome_email(email)
        return True
    return False


def send_welcome_email(email):
    """Placeholder - in real code, this would send email"""
    print(f"Sending email to {email}")


# FIX: Separate validation from action
def validate_email_fixed(email: str) -> bool:
    """Just validates, doesn't send"""
    return "@" in email and "." in email


def process_new_user(email: str) -> bool:
    """Orchestrates validation AND sending"""
    if validate_email_fixed(email):
        send_welcome_email(email)
        return True
    return False


# =============================================================================
# BUG #2: Get Function That Deletes
# =============================================================================
# HARMONIZER SCORE: ~0.95 (!! CRITICAL DISHARMONY)
# OTHER TOOLS: All pass ✓


def get_user_by_id(user_id: int):
    """
    BUG: Function claims to GET, but actually DELETES!

    Harmonizer catches:
    - "get" = Wisdom (read operation)
    - "delete" = Power (destructive operation)
    - CRITICAL semantic contradiction

    Real-world impact:
    - Developer calls get_user_by_id() expecting read-only
    - Data gets deleted unexpectedly
    - Could cause data loss in production
    """
    # Connect to database
    db = get_database_connection()

    # VIOLATION: Should query, not delete!
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return user_id


def get_database_connection():
    """Placeholder"""

    class FakeDB:
        def execute(self, query):
            print(f"Executing: {query}")

    return FakeDB()


# FIX: Name matches behavior
def delete_user_by_id(user_id: int):
    """Honestly named - clearly destructive"""
    db = get_database_connection()
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    return user_id


def get_user_by_id_fixed(user_id: int):
    """Actually gets without modifying"""
    db = get_database_connection()
    # Now it actually queries, doesn't delete
    result = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return result


# =============================================================================
# BUG #3: Check Function That Creates
# =============================================================================
# HARMONIZER SCORE: ~0.75 (!! DISHARMONY)
# OTHER TOOLS: Might pass


def check_file_exists(filepath: str) -> bool:
    """
    BUG: Function claims to check, but creates if missing!

    Harmonizer catches:
    - "check" = Wisdom (read/verify)
    - "create" = Power (write/modify)
    - Side effect hidden in name

    Why this is dangerous:
    - Caller expects read-only check
    - Filesystem gets modified unexpectedly
    - Could create files in wrong locations
    """
    import os

    if not os.path.exists(filepath):
        # VIOLATION: Check functions shouldn't create!
        with open(filepath, "w") as f:
            f.write("")
        return False
    return True


# FIX: Separate check from creation
def check_file_exists_fixed(filepath: str) -> bool:
    """Pure check - no side effects"""
    import os

    return os.path.exists(filepath)


def ensure_file_exists(filepath: str) -> bool:
    """Honest name - creates if missing"""
    import os

    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("")
        return False
    return True


# =============================================================================
# BUG #4: Calculate Function That Saves
# =============================================================================
# HARMONIZER SCORE: ~0.70 (!! DISHARMONY)
# OTHER TOOLS: Tests might pass if they expect side effects


def calculate_total_price(items: list) -> float:
    """
    BUG: Function claims to calculate, but also saves to database!

    Harmonizer catches:
    - "calculate" = Wisdom (computation)
    - "save" = Power (persistence)
    - Mixed concerns

    Problems:
    - Can't calculate without database
    - Unexpected persistence
    - Hard to test
    - Violates single responsibility
    """
    total = sum(item["price"] for item in items)

    # VIOLATION: Calculate functions shouldn't persist!
    save_to_database("total_price", total)

    return total


def save_to_database(key, value):
    """Placeholder"""
    print(f"Saving {key} = {value} to database")


# FIX: Separate calculation from persistence
def calculate_total_price_fixed(items: list) -> float:
    """Pure calculation - no side effects"""
    return sum(item["price"] for item in items)


def calculate_and_save_total_price(items: list) -> float:
    """Honest name - calculates AND saves"""
    total = calculate_total_price_fixed(items)
    save_to_database("total_price", total)
    return total


# =============================================================================
# BUG #5: Read Function That Updates
# =============================================================================
# HARMONIZER SCORE: ~0.80 (!! DISHARMONY)
# OTHER TOOLS: Hard to catch without semantic analysis


def read_configuration(config_file: str) -> dict:
    """
    BUG: Function claims to read, but updates last_accessed timestamp!

    Harmonizer catches:
    - "read" = Wisdom (non-modifying)
    - "update" = Power (modifying)
    - Hidden side effect

    Why subtle:
    - Seems harmless (just a timestamp)
    - But violates principle of least surprise
    - Could cause issues with file permissions
    - Prevents true read-only access
    """
    import json

    with open(config_file, "r") as f:
        config = json.load(f)

    # VIOLATION: Read functions shouldn't modify!
    update_last_accessed_timestamp(config_file)

    return config


def update_last_accessed_timestamp(filepath):
    """Placeholder"""
    import time

    print(f"Updating timestamp for {filepath} to {time.time()}")


# FIX: Either truly read-only OR honest name
def read_configuration_fixed(config_file: str) -> dict:
    """Pure read - no side effects"""
    import json

    with open(config_file, "r") as f:
        return json.load(f)


def read_and_track_configuration(config_file: str) -> dict:
    """Honest name - reads AND tracks access"""
    config = read_configuration_fixed(config_file)
    update_last_accessed_timestamp(config_file)
    return config


# =============================================================================
# BUG #6: Filter Function That Deletes
# =============================================================================
# HARMONIZER SCORE: ~0.90 (!! CRITICAL DISHARMONY)
# OTHER TOOLS: Might not catch unless tests verify original list unchanged


def filter_invalid_users(users: list) -> list:
    """
    BUG: Function claims to filter (read), but deletes from database!

    Harmonizer catches:
    - "filter" = Wisdom (selection/reading)
    - "delete" = Power (destructive)
    - Critical contradiction

    Expected: Return filtered list
    Actual: Modifies database!

    Real-world disaster:
    - Developer expects non-destructive filtering
    - Users get deleted from production database
    - Data loss
    """
    valid_users = []

    for user in users:
        if user["email"] and user["name"]:
            valid_users.append(user)
        else:
            # VIOLATION: Filter shouldn't delete from DB!
            delete_user_from_database(user["id"])

    return valid_users


def delete_user_from_database(user_id):
    """Placeholder"""
    print(f"DELETING user {user_id} from database!")


# FIX: Separate filtering from deletion
def filter_invalid_users_fixed(users: list) -> list:
    """Pure filter - no side effects"""
    return [u for u in users if u["email"] and u["name"]]


def remove_invalid_users(users: list) -> list:
    """Honest name - filters AND deletes from database"""
    valid_users = []

    for user in users:
        if user["email"] and user["name"]:
            valid_users.append(user)
        else:
            delete_user_from_database(user["id"])

    return valid_users


# =============================================================================
# BUG #7: Log Function That Raises
# =============================================================================
# HARMONIZER SCORE: ~0.65 (!! DISHARMONY)
# OTHER TOOLS: Tests might catch if they expect no exceptions


def log_error_message(message: str):
    """
    BUG: Function claims to log, but raises exception!

    Harmonizer catches:
    - "log" = Wisdom (recording/passive)
    - "raise" = Power (control flow change)
    - Unexpected behavior

    Problems:
    - Caller expects logging to be safe
    - Exception disrupts program flow
    - Violates principle of least surprise
    """
    print(f"ERROR: {message}")

    # VIOLATION: Log functions shouldn't raise!
    if "critical" in message.lower():
        raise RuntimeError(f"Critical error: {message}")


# FIX: Either log OR raise, not both under "log" name
def log_error_message_fixed(message: str):
    """Just logs - never raises"""
    print(f"ERROR: {message}")


def handle_error_message(message: str):
    """Honest name - logs AND may raise"""
    print(f"ERROR: {message}")

    if "critical" in message.lower():
        raise RuntimeError(f"Critical error: {message}")


# =============================================================================
# Summary
# =============================================================================

"""
KEY INSIGHTS:

1. **All these bugs pass traditional tools:**
   - Syntax is valid
   - Types are correct (if using type hints)
   - Tests might pass (if they expect the behavior)
   - Linters see no style violations

2. **Harmonizer catches them because:**
   - Analyzes semantic meaning
   - Compares name intent vs actual behavior
   - Detects contradictions between read/write operations

3. **Common patterns:**
   - Validation functions that modify
   - Get/Read functions that delete/update
   - Check/Filter functions that create/destroy
   - Calculate/Log functions with side effects

4. **Real-world impact:**
   - Data loss
   - Unexpected side effects
   - Violation of least surprise principle
   - Harder to reason about code
   - Maintenance nightmares

5. **The fix is always:**
   - Make the name match the behavior, OR
   - Make the behavior match the name, OR
   - Split into two functions with honest names

Run this file through Harmonizer:
    harmonizer examples/real_world_bugs.py

You'll see disharmony scores for all the buggy functions,
while the fixed versions show excellent harmony!
"""

# =============================================================================
# Test Helper
# =============================================================================

if __name__ == "__main__":
    print("🔍 Real-World Semantic Bugs Demo")
    print("=" * 70)
    print("\nThese bugs would slip past traditional tools!")
    print("Run: harmonizer examples/real_world_bugs.py")
    print("\nExpect HIGH disharmony scores for:")
    print("  - validate_email (sends emails)")
    print("  - get_user_by_id (deletes data)")
    print("  - check_file_exists (creates files)")
    print("  - calculate_total_price (saves to DB)")
    print("  - read_configuration (updates timestamps)")
    print("  - filter_invalid_users (deletes from DB)")
    print("  - log_error_message (raises exceptions)")
    print("\nExpect LOW scores for the _fixed versions!")
    print("=" * 70)
