"""
Severity Levels: Examples at Each Score Range

This file demonstrates functions at each severity level:
- EXCELLENT: 0.0 - 0.3
- LOW: 0.3 - 0.5
- MEDIUM: 0.5 - 0.8
- HIGH: 0.8 - 1.0
- CRITICAL: 1.0+

Run: harmonizer examples/severity_levels.py

You'll see the full spectrum from perfect harmony to critical disharmony.
"""

# =============================================================================
# EXCELLENT HARMONY: Score 0.0 - 0.3
# =============================================================================
# These functions have perfect or near-perfect semantic alignment.
# Name matches implementation beautifully.
# No action needed - keep this quality!

print("\n" + "=" * 70)
print("EXCELLENT HARMONY (0.0 - 0.3)")
print("=" * 70)


def create_user_account(username, email):
    """
    Expected score: ~0.05

    Perfect alignment:
    - Name: 'create' (Power dimension)
    - Actions: 'build', 'save', 'initialize' (Power dimension)
    - All operations support user creation
    - Semantic harmony ✓
    """
    user_data = build_user_object(username, email)
    save_to_database(user_data)
    initialize_user_preferences(user_data)
    return user_data


def calculate_total_amount(items):
    """
    Expected score: ~0.08

    Strong alignment:
    - Name: 'calculate' (Wisdom dimension)
    - Actions: 'sum', 'compute' (Wisdom dimension)
    - Pure calculation, no side effects
    - Self-documenting code ✓
    """
    return sum(item["price"] for item in items)


def validate_email_format(email):
    """
    Expected score: ~0.10

    Excellent harmony:
    - Name: 'validate' (Wisdom - checking)
    - Actions: 'check', 'verify' (Wisdom)
    - Returns boolean
    - No modifications ✓
    """
    return "@" in email and "." in email.split("@")[1]


def delete_temporary_files(directory):
    """
    Expected score: ~0.12

    Clear intent:
    - Name: 'delete' (Power - destructive)
    - Actions: 'remove', 'clean' (Power)
    - Honest about destructive nature
    - No surprises ✓
    """
    import os

    for file in os.listdir(directory):
        if file.endswith(".tmp"):
            remove_file(os.path.join(directory, file))


def query_user_by_id(user_id):
    """
    Expected score: ~0.15

    Good alignment:
    - Name: 'query' (Wisdom - reading)
    - Actions: 'fetch', 'retrieve' (Wisdom)
    - Read-only operation
    - Returns data ✓
    """
    return fetch_from_database("users", user_id)


# =============================================================================
# LOW CONCERN: Score 0.3 - 0.5
# =============================================================================
# Slight semantic misalignment, but generally acceptable.
# Consider refactoring if you have time.
# Monitor to prevent drift.

print("\n" + "=" * 70)
print("LOW CONCERN (0.3 - 0.5)")
print("=" * 70)


def process_payment(payment_data):
    """
    Expected score: ~0.35

    Minor issue:
    - Name: 'process' (somewhat vague)
    - Actions: 'validate', 'charge', 'record' (mixed operations)
    - Works, but 'process' is generic
    - Consider: 'execute_payment_transaction' for clarity
    """
    validate_payment_data(payment_data)
    charge_credit_card(payment_data)
    record_transaction(payment_data)
    return True


def get_or_create_session(user_id):
    """
    Expected score: ~0.40

    Acceptable mixed semantics:
    - Name explicitly says: 'get' OR 'create'
    - Honest about dual purpose
    - Developer knows to expect modification
    - But: Consider splitting if possible
    """
    session = get_existing_session(user_id)
    if not session:
        session = create_new_session(user_id)
    return session


def update_user_profile(user_id, data):
    """
    Expected score: ~0.38

    Slight vagueness:
    - Name: 'update' (clear intent)
    - Actions: 'merge', 'save', 'validate' (mostly aligned)
    - Minor: validation before update adds slight distance
    - Could be: 'validate_and_update_profile' for precision
    """
    validate_profile_data(data)
    current = get_user_profile(user_id)
    merged = merge_profile_data(current, data)
    save_profile(user_id, merged)


def handle_error_gracefully(error):
    """
    Expected score: ~0.42

    Generic but acceptable:
    - Name: 'handle' (vague)
    - Actions: 'log', 'format', 'return' (specific)
    - Works for error handling context
    - Consider: 'log_and_format_error' for specificity
    """
    log_error_to_file(error)
    formatted = format_error_message(error)
    return formatted


def check_and_initialize_config(config_path):
    """
    Expected score: ~0.45

    Borderline acceptable:
    - Name: explicitly 'check AND initialize'
    - Honest about dual purpose
    - But: violates single responsibility
    - Better: Separate check_config() and initialize_config()
    """
    if not config_exists(config_path):
        initialize_default_config(config_path)
    return load_config(config_path)


# =============================================================================
# MEDIUM CONCERN: Score 0.5 - 0.8
# =============================================================================
# Significant semantic misalignment.
# Should refactor when you can.
# Potential for confusion and bugs.

print("\n" + "=" * 70)
print("MEDIUM CONCERN (0.5 - 0.8)")
print("=" * 70)


def validate_user_credentials(username, password):
    """
    Expected score: ~0.55

    Problem:
    - Name: 'validate' (checking/reading)
    - Actions: 'update_last_login' (writing/modifying)
    - Side effect hidden in validation
    - Should: Separate validate from tracking
    """
    is_valid = check_credentials(username, password)
    if is_valid:
        # ISSUE: Validation shouldn't modify!
        update_last_login(username)
    return is_valid


def get_user_preferences(user_id):
    """
    Expected score: ~0.60

    Problem:
    - Name: 'get' (read-only expectation)
    - Actions: 'create_default_if_missing' (write operation)
    - Surprising side effect
    - Should: Either truly read-only OR rename to 'ensure_preferences'
    """
    prefs = fetch_preferences(user_id)
    if not prefs:
        # ISSUE: Get shouldn't create!
        prefs = create_default_preferences(user_id)
        save_preferences(user_id, prefs)
    return prefs


def calculate_and_cache_result(input_data):
    """
    Expected score: ~0.58

    Problem:
    - Name says: 'calculate AND cache' (mixed)
    - Violates single responsibility
    - Hard to test calculation separately
    - Should: Separate calculate() from cache management
    """
    result = perform_calculation(input_data)
    # Mixed: calculation with caching
    store_in_cache(input_data, result)
    return result


def process_order(order_data):
    """
    Expected score: ~0.65

    Problem:
    - Name: 'process' (too vague)
    - Actions: validate, charge, ship, email (many operations)
    - God function - does too much
    - Should: Break into pipeline with orchestrator
    """
    validate_order(order_data)
    charge_payment(order_data)
    ship_items(order_data)
    send_confirmation_email(order_data)
    return True


def load_configuration_file(filepath):
    """
    Expected score: ~0.62

    Problem:
    - Name: 'load' (reading)
    - Actions: 'parse', 'validate', 'apply_defaults', 'save_back'
    - Modifies file when loading!
    - Should: Separate load from modification
    """
    config = parse_config_file(filepath)
    config = apply_default_values(config)
    # ISSUE: Load shouldn't save!
    save_config_file(filepath, config)
    return config


# =============================================================================
# HIGH CONCERN: Score 0.8 - 1.0
# =============================================================================
# Severe semantic contradiction.
# Refactor immediately.
# High risk of bugs and confusion.

print("\n" + "=" * 70)
print("HIGH CONCERN (0.8 - 1.0)")
print("=" * 70)


def read_log_file(logfile_path):
    """
    Expected score: ~0.82

    SEVERE PROBLEM:
    - Name: 'read' (non-destructive)
    - Actions: 'clear_after_reading' (destructive!)
    - CRITICAL: Developer expects safe read
    - Reality: File gets cleared!
    - FIX: Rename to 'read_and_clear_log' OR remove clearing
    """
    with open(logfile_path, "r") as f:
        contents = f.read()

    # VIOLATION: Read shouldn't clear!
    clear_log_file(logfile_path)

    return contents


def check_inventory_level(product_id):
    """
    Expected score: ~0.85

    SEVERE PROBLEM:
    - Name: 'check' (read-only)
    - Actions: 'reorder_if_low' (write/action)
    - Hidden side effect: places orders!
    - FIX: Separate check from reordering logic
    """
    level = get_inventory_count(product_id)

    # VIOLATION: Check shouldn't trigger reorders!
    if level < 10:
        trigger_reorder(product_id)

    return level


def log_transaction(transaction_data):
    """
    Expected score: ~0.88

    SEVERE PROBLEM:
    - Name: 'log' (passive recording)
    - Actions: 'raise exception' (control flow change)
    - Caller expects logging to be safe
    - Reality: Can crash the program!
    - FIX: Either log OR validate separately
    """
    write_to_log(transaction_data)

    # VIOLATION: Log shouldn't raise!
    if transaction_data["amount"] > 10000:
        raise ValueError("Transaction too large!")


def filter_active_users(users_list):
    """
    Expected score: ~0.90

    CRITICAL PROBLEM:
    - Name: 'filter' (non-destructive selection)
    - Actions: 'delete_inactive_from_db' (destructive!)
    - Developer expects list filtering
    - Reality: Database gets modified!
    - FIX: Separate filtering from database operations
    """
    active = []
    for user in users_list:
        if user["is_active"]:
            active.append(user)
        else:
            # VIOLATION: Filter shouldn't delete from DB!
            delete_from_database(user["id"])

    return active


def get_cache_value(cache_key):
    """
    Expected score: ~0.87

    CRITICAL PROBLEM:
    - Name: 'get' (read-only)
    - Actions: 'fetch_from_api' if missing (network call!)
    - Developer expects fast cache lookup
    - Reality: Might make slow API call!
    - FIX: Rename to 'get_or_fetch_value' or separate concerns
    """
    if cache_key in cache:
        return cache[cache_key]

    # VIOLATION: Get shouldn't make API calls!
    value = fetch_from_external_api(cache_key)
    cache[cache_key] = value

    return value


# =============================================================================
# CRITICAL CONCERN: Score 1.0+
# =============================================================================
# Extreme semantic contradiction.
# **IMMEDIATE ACTION REQUIRED**
# Very high risk - could cause data loss or security issues.

print("\n" + "=" * 70)
print("CRITICAL CONCERN (1.0+)")
print("=" * 70)


def validate_password(password):
    """
    Expected score: ~1.05

    CRITICAL EMERGENCY:
    - Name: 'validate' (checking)
    - Actions: 'delete_user_account' (destructive!)
    - Complete semantic opposite
    - Developer expects password check
    - Reality: DELETES ACCOUNTS!
    - FIX IMMEDIATELY: This is a catastrophic bug
    """
    if len(password) < 8:
        # CATASTROPHIC: Validation shouldn't delete users!
        delete_user_account_for_weak_password()
        return False
    return True


def get_user_data(user_id):
    """
    Expected score: ~1.02

    CRITICAL EMERGENCY:
    - Name: 'get' (read operation)
    - Actions: 'delete_user' (destructive operation)
    - Semantic opposite: read vs destroy
    - DATA LOSS RISK
    - FIX IMMEDIATELY: Rename or remove deletion
    """
    user = fetch_user(user_id)

    # CATASTROPHIC: Get shouldn't delete!
    delete_user_from_database(user_id)

    return user


def save_preferences(user_id, preferences):
    """
    Expected score: ~0.98

    CRITICAL PROBLEM:
    - Name: 'save' (write/persist)
    - Actions: 'send_email_notifications' (communication)
    - Unexpected external communication
    - Privacy/security risk
    - FIX IMMEDIATELY: Remove email from save operation
    """
    store_preferences(user_id, preferences)

    # VIOLATION: Save shouldn't send emails!
    # Privacy issue: saving preferences shouldn't notify others
    send_email_to_all_admins(f"User {user_id} changed preferences")


def query_database(sql_query):
    """
    Expected score: ~1.10

    CRITICAL SECURITY RISK:
    - Name: 'query' (read-only SELECT)
    - Actions: Actually executes ANY SQL including DROP, DELETE
    - Developer expects safe read
    - Reality: Can destroy entire database!
    - FIX IMMEDIATELY: Validate query type or rename
    """
    # CATASTROPHIC: Query should only SELECT!
    # This could execute: DROP TABLE users;
    execute_raw_sql(sql_query)

    return fetch_results()


def check_permission(user_id, resource):
    """
    Expected score: ~1.15

    CRITICAL SECURITY RISK:
    - Name: 'check' (read-only verification)
    - Actions: 'grant_admin_if_missing' (privilege escalation!)
    - Security nightmare: checking grants access!
    - FIX IMMEDIATELY: Never mix checking with granting
    """
    has_permission = verify_user_access(user_id, resource)

    if not has_permission:
        # SECURITY VIOLATION: Check shouldn't grant access!
        grant_admin_privileges(user_id)
        has_permission = True

    return has_permission


# =============================================================================
# Placeholder Functions
# =============================================================================


def build_user_object(username, email):
    return {"username": username, "email": email}


def save_to_database(data):
    print(f"Saving to database: {data}")


def initialize_user_preferences(user):
    print(f"Initializing preferences for {user['username']}")


def remove_file(filepath):
    print(f"Removing file: {filepath}")


def fetch_from_database(table, id):
    return {"id": id, "data": "sample"}


def validate_payment_data(data):
    return True


def charge_credit_card(data):
    print("Charging credit card")


def record_transaction(data):
    print("Recording transaction")


def get_existing_session(user_id):
    return None


def create_new_session(user_id):
    return {"user_id": user_id, "session_id": "abc123"}


def validate_profile_data(data):
    return True


def get_user_profile(user_id):
    return {"name": "User"}


def merge_profile_data(current, new):
    return {**current, **new}


def save_profile(user_id, data):
    print(f"Saving profile for user {user_id}")


def log_error_to_file(error):
    print(f"Logging error: {error}")


def format_error_message(error):
    return str(error)


def config_exists(path):
    return False


def initialize_default_config(path):
    print(f"Initializing config at {path}")


def load_config(path):
    return {"setting": "value"}


def check_credentials(username, password):
    return True


def update_last_login(username):
    print(f"Updating last login for {username}")


def fetch_preferences(user_id):
    return None


def create_default_preferences(user_id):
    return {"theme": "light"}


def save_preferences(user_id, prefs):
    print(f"Saving preferences for user {user_id}")


def perform_calculation(data):
    return 42


def store_in_cache(key, value):
    print(f"Caching {key} = {value}")


def validate_order(data):
    print("Validating order")


def charge_payment(data):
    print("Charging payment")


def ship_items(data):
    print("Shipping items")


def send_confirmation_email(data):
    print("Sending confirmation email")


def parse_config_file(path):
    return {}


def apply_default_values(config):
    return config


def save_config_file(path, config):
    print(f"Saving config to {path}")


def clear_log_file(path):
    print(f"CLEARING log file: {path}")


def get_inventory_count(product_id):
    return 5


def trigger_reorder(product_id):
    print(f"TRIGGERING REORDER for product {product_id}")


def write_to_log(data):
    print(f"Logging: {data}")


def delete_from_database(id):
    print(f"DELETING from database: ID {id}")


cache = {}


def fetch_from_external_api(key):
    print(f"FETCHING from external API: {key}")
    return "api_value"


def delete_user_account_for_weak_password():
    print("CATASTROPHIC: DELETING USER ACCOUNT!")


def fetch_user(user_id):
    return {"id": user_id, "name": "User"}


def delete_user_from_database(user_id):
    print(f"CATASTROPHIC: DELETING USER {user_id}!")


def store_preferences(user_id, prefs):
    print(f"Storing preferences for {user_id}")


def send_email_to_all_admins(message):
    print(f"SENDING EMAIL TO ADMINS: {message}")


def execute_raw_sql(query):
    print(f"EXECUTING RAW SQL: {query}")


def fetch_results():
    return []


def verify_user_access(user_id, resource):
    return False


def grant_admin_privileges(user_id):
    print(f"SECURITY VIOLATION: GRANTING ADMIN TO {user_id}!")


# =============================================================================
# Summary and Guidance
# =============================================================================

"""
SEVERITY LEVEL GUIDE:

📗 EXCELLENT (0.0 - 0.3)
   ✓ Perfect semantic alignment
   ✓ Self-documenting code
   ✓ No action needed
   ✓ Example: create_user(), validate_email()

📘 LOW (0.3 - 0.5)
   ⚠ Minor semantic drift
   ⚠ Consider refactoring when convenient
   ⚠ Monitor to prevent worsening
   ⚠ Example: process_payment(), get_or_create()

📙 MEDIUM (0.5 - 0.8)
   ⚠️ Significant misalignment
   ⚠️ Should refactor soon
   ⚠️ Risk of confusion
   ⚠️ Example: validate() that modifies, get() that creates

📕 HIGH (0.8 - 1.0)
   🚨 Severe contradiction
   🚨 Refactor immediately
   🚨 High bug risk
   🚨 Example: read() that deletes, check() that triggers actions

📕 CRITICAL (1.0+)
   🔥 EMERGENCY - FIX NOW
   🔥 Semantic opposite
   🔥 Data loss / security risk
   🔥 Example: validate() that deletes accounts, get() that destroys data

TRIAGE PRIORITY:

1. Fix CRITICAL immediately (1.0+) - these are emergencies
2. Fix HIGH next (0.8-1.0) - schedule within days
3. Fix MEDIUM when refactoring (0.5-0.8) - next sprint
4. Fix LOW opportunistically (0.3-0.5) - when touching the code
5. Maintain EXCELLENT (0.0-0.3) - use as examples

TEAM STANDARDS:

Suggested thresholds:
- Block CI/CD if score > 0.8 (HIGH/CRITICAL)
- Warn on PR if score > 0.5 (MEDIUM+)
- Set goal: all functions < 0.3 (EXCELLENT)

Run this file:
    harmonizer examples/severity_levels.py

You'll see the full range from excellent to critical! 💛⚓
"""

# =============================================================================
# Run This Example
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SEVERITY LEVELS DEMONSTRATION")
    print("=" * 70)
    print("\nThis file contains functions at every severity level:")
    print("\n  📗 EXCELLENT (0.0-0.3):  Perfect alignment")
    print("  📘 LOW (0.3-0.5):        Minor issues")
    print("  📙 MEDIUM (0.5-0.8):     Significant problems")
    print("  📕 HIGH (0.8-1.0):       Severe contradictions")
    print("  🔥 CRITICAL (1.0+):      EMERGENCIES")
    print("\nRun: harmonizer examples/severity_levels.py")
    print("\nUse this as a reference for prioritizing refactoring!")
    print("=" * 70 + "\n")
