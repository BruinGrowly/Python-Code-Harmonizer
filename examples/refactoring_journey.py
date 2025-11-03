"""
Refactoring Journey: Before & After with Harmonizer Scores

This file demonstrates the refactoring journey using Harmonizer as a guide.
Each example shows:
1. BEFORE: Disharmonious code with high score
2. Harmonizer analysis
3. Refactoring steps
4. AFTER: Harmonious code with low score

Run sections separately to see score differences:
    harmonizer examples/refactoring_journey.py
"""

# =============================================================================
# JOURNEY #1: User Management Refactoring
# =============================================================================

print("\n" + "=" * 70)
print("JOURNEY #1: From 'process' to clear intent")
print("=" * 70)

# -----------------------------------------------------------------------------
# BEFORE - Disharmony Score: ~0.75
# -----------------------------------------------------------------------------


def process_user(user_data):
    """
    PROBLEM: 'process' is vague
    - What kind of processing?
    - Read or write operation?
    - Creates confusion

    Harmonizer flags this because:
    - 'process' = low semantic value
    - 'create', 'save', 'send' = specific operations
    - Distance between vague and specific = disharmony
    """
    # Creates new user
    user = create_user_record(user_data)

    # Saves to database
    save_to_database(user)

    # Sends welcome email
    send_welcome_email(user["email"])

    return user


# -----------------------------------------------------------------------------
# REFACTORING STEPS
# -----------------------------------------------------------------------------

# Step 1: Identify what it actually does
# - Creates user record
# - Saves to database
# - Sends email
# → This is USER REGISTRATION, not generic "processing"

# Step 2: Split into focused functions
# Step 3: Use descriptive names

# -----------------------------------------------------------------------------
# AFTER - Disharmony Score: ~0.15 (Excellent!)
# -----------------------------------------------------------------------------


def register_new_user(user_data):
    """
    SOLUTION: Name describes exact behavior

    Improvements:
    - 'register' clearly indicates creating + setting up
    - Matches actual operations
    - Self-documenting

    Harmonizer loves this because:
    - 'register' aligns with 'create', 'save', 'send'
    - All operations support user registration
    - Low semantic distance = harmony
    """
    user = create_user_record(user_data)
    save_to_database(user)
    send_welcome_email(user["email"])
    return user


# =============================================================================
# JOURNEY #2: Data Retrieval Refactoring
# =============================================================================

print("\n" + "=" * 70)
print("JOURNEY #2: From misleading to honest")
print("=" * 70)

# -----------------------------------------------------------------------------
# BEFORE - Disharmony Score: ~0.90 (Critical!)
# -----------------------------------------------------------------------------


def get_user_settings(user_id):
    """
    PROBLEM: Says 'get' but actually modifies!

    Harmonizer catches:
    - 'get' = Wisdom (read operation)
    - 'update' = Power (write operation)
    - CRITICAL contradiction

    Developer expects:
    - Read-only operation
    - No side effects
    - Safe to call multiple times

    Reality:
    - Modifies last_login
    - Updates analytics
    - Side effects!
    """
    settings = query_settings_from_db(user_id)

    # VIOLATION: Get functions shouldn't modify!
    update_last_login(user_id)
    increment_analytics_counter(user_id)

    return settings


# -----------------------------------------------------------------------------
# REFACTORING STEPS
# -----------------------------------------------------------------------------

# Step 1: Separate read from write
# Step 2: Make get() truly read-only
# Step 3: Create separate function for tracking

# -----------------------------------------------------------------------------
# AFTER - Disharmony Score: ~0.10 (Excellent!)
# -----------------------------------------------------------------------------


def get_user_settings(user_id):  # noqa: F811
    """
    SOLUTION: Pure read operation

    Now it's truly a 'get':
    - Read-only
    - No side effects
    - Harmonizer score: excellent
    """
    return query_settings_from_db(user_id)


def track_settings_access(user_id):
    """
    SOLUTION: Separate tracking function

    Honest about side effects:
    - Name clearly indicates modification
    - Can be called separately
    - Single responsibility
    """
    update_last_login(user_id)
    increment_analytics_counter(user_id)


def get_and_track_settings(user_id):
    """
    SOLUTION: Orchestrator with honest name

    If you need both:
    - Name indicates both operations
    - Composes smaller functions
    - Clear intent
    """
    settings = get_user_settings(user_id)
    track_settings_access(user_id)
    return settings


# =============================================================================
# JOURNEY #3: Validation Logic Refactoring
# =============================================================================

print("\n" + "=" * 70)
print("JOURNEY #3: From overgrown to focused")
print("=" * 70)

# -----------------------------------------------------------------------------
# BEFORE - Disharmony Score: ~0.70
# -----------------------------------------------------------------------------


def validate_input(data):
    """
    PROBLEM: Function grew beyond its name

    Started as simple validation, but grew to include:
    - Validation (checking)
    - Sanitization (modifying)
    - Formatting (transforming)
    - Logging (side effects)

    Harmonizer detects:
    - 'validate' = Wisdom (checking)
    - 'sanitize', 'format', 'log' = mixed semantics
    - Function does too much
    """
    # Validation
    if not data:
        log_validation_error("Empty data")
        return False

    # Sanitization (modifying!)
    data = sanitize_sql_injection(data)

    # Formatting (transforming!)
    data = format_to_lowercase(data)

    # More validation
    if len(data) < 3:
        log_validation_error("Too short")
        return False

    return True


# -----------------------------------------------------------------------------
# REFACTORING STEPS
# -----------------------------------------------------------------------------

# Step 1: Separate validation from transformation
# Step 2: Separate logging from validation
# Step 3: Create pipeline with clear steps

# -----------------------------------------------------------------------------
# AFTER - Disharmony Scores: All ~0.05-0.20 (Excellent!)
# -----------------------------------------------------------------------------


def validate_input(data):  # noqa: F811
    """
    SOLUTION: Pure validation

    Now it ONLY validates:
    - No modifications
    - No side effects
    - Returns bool
    - Harmonizer: excellent score
    """
    if not data:
        return False
    if len(data) < 3:
        return False
    return True


def sanitize_input(data):
    """
    SOLUTION: Pure sanitization

    Focused responsibility:
    - Removes dangerous characters
    - Returns cleaned data
    - Name matches behavior
    """
    return sanitize_sql_injection(data)


def format_input(data):
    """
    SOLUTION: Pure formatting

    Single purpose:
    - Transforms to lowercase
    - Returns formatted data
    - Clear intent
    """
    return format_to_lowercase(data)


def process_user_input(data):
    """
    SOLUTION: Orchestrator with honest name

    Now 'process' is appropriate because:
    - Explicitly multi-step
    - Combines validate + sanitize + format
    - Name indicates complex operation
    """
    if not validate_input(data):
        log_validation_error("Validation failed")
        return None

    data = sanitize_input(data)
    data = format_input(data)

    return data


# =============================================================================
# JOURNEY #4: Resource Management Refactoring
# =============================================================================

print("\n" + "=" * 70)
print("JOURNEY #4: From surprising to expected")
print("=" * 70)

# -----------------------------------------------------------------------------
# BEFORE - Disharmony Score: ~0.80
# -----------------------------------------------------------------------------


def check_cache_available(cache_key):
    """
    PROBLEM: Hidden side effect

    Harmonizer catches:
    - 'check' = Wisdom (read/verify)
    - 'initialize', 'create' = Power (write/modify)
    - Unexpected behavior

    Developer expects:
    - Simple boolean check
    - No modifications

    Reality:
    - Creates cache if missing
    - Initializes default values
    - Side effects!
    """
    if cache_key in cache_store:
        return True

    # VIOLATION: Check functions shouldn't create!
    initialize_cache(cache_key)
    create_default_values(cache_key)

    return False


# -----------------------------------------------------------------------------
# REFACTORING STEPS
# -----------------------------------------------------------------------------

# Step 1: Separate checking from creation
# Step 2: Use explicit names
# Step 3: Provide both options

# -----------------------------------------------------------------------------
# AFTER - Disharmony Scores: ~0.05-0.15 (Excellent!)
# -----------------------------------------------------------------------------


def check_cache_available(cache_key):  # noqa: F811
    """
    SOLUTION: Pure check

    Now truly a check:
    - Read-only
    - No side effects
    - Returns simple boolean
    """
    return cache_key in cache_store


def initialize_cache_if_missing(cache_key):
    """
    SOLUTION: Explicit initialization

    Honest name:
    - Clearly indicates creation
    - Developer knows what to expect
    - No surprises
    """
    if cache_key not in cache_store:
        initialize_cache(cache_key)
        create_default_values(cache_key)
    return True


def ensure_cache_ready(cache_key):
    """
    SOLUTION: Alternative with clear intent

    'ensure' is perfect because:
    - Implies it will create if needed
    - Guarantees cache exists after call
    - Semantic harmony with actions
    """
    if not check_cache_available(cache_key):
        initialize_cache_if_missing(cache_key)
    return True


# =============================================================================
# JOURNEY #5: API Endpoint Refactoring
# =============================================================================

print("\n" + "=" * 70)
print("JOURNEY #5: From overloaded to specialized")
print("=" * 70)

# -----------------------------------------------------------------------------
# BEFORE - Disharmony Score: ~0.85
# -----------------------------------------------------------------------------


def handle_request(request_data):
    """
    PROBLEM: One function doing everything

    Issues:
    - 'handle' is too vague
    - Parses, validates, processes, responds
    - Hard to test
    - Hard to maintain

    Harmonizer sees:
    - Generic 'handle'
    - Specific 'parse', 'validate', 'execute', 'format'
    - High semantic distance
    """
    # Parse
    data = parse_json(request_data)

    # Validate
    if not is_valid(data):
        return error_response("Invalid")

    # Execute business logic
    result = execute_business_logic(data)

    # Format response
    response = format_json_response(result)

    # Log
    log_request(request_data)

    return response


# -----------------------------------------------------------------------------
# REFACTORING STEPS
# -----------------------------------------------------------------------------

# Step 1: Break into pipeline stages
# Step 2: Each function has clear responsibility
# Step 3: Compose with orchestrator

# -----------------------------------------------------------------------------
# AFTER - Disharmony Scores: All ~0.05-0.20 (Excellent!)
# -----------------------------------------------------------------------------


def parse_request(request_data):
    """Stage 1: Parsing"""
    return parse_json(request_data)


def validate_request(data):
    """Stage 2: Validation"""
    return is_valid(data)


def execute_request(data):
    """Stage 3: Business logic"""
    return execute_business_logic(data)


def format_response(result):
    """Stage 4: Response formatting"""
    return format_json_response(result)


def log_request_processed(request_data):
    """Side effect: Logging"""
    log_request(request_data)


def process_api_request(request_data):
    """
    SOLUTION: Clear orchestration

    Now 'process' is appropriate because:
    - Name indicates multi-step operation
    - Each step is clearly defined
    - Easy to test each stage
    - Easy to modify pipeline
    """
    # Parse
    data = parse_request(request_data)

    # Validate
    if not validate_request(data):
        return error_response("Invalid")

    # Execute
    result = execute_request(data)

    # Log
    log_request_processed(request_data)

    # Format and return
    return format_response(result)


# =============================================================================
# Placeholder Functions (for examples to run)
# =============================================================================


def create_user_record(data):
    return {"id": 1, "email": data.get("email", "test@example.com")}


def save_to_database(user):
    print(f"Saving user {user['id']} to database")


def send_welcome_email(email):
    print(f"Sending welcome email to {email}")


def query_settings_from_db(user_id):
    return {"theme": "dark", "language": "en"}


def update_last_login(user_id):
    print(f"Updating last login for user {user_id}")


def increment_analytics_counter(user_id):
    print(f"Incrementing analytics for user {user_id}")


def log_validation_error(message):
    print(f"VALIDATION ERROR: {message}")


def sanitize_sql_injection(data):
    return data.replace("'", "''")


def format_to_lowercase(data):
    return data.lower()


cache_store = {}


def initialize_cache(key):
    cache_store[key] = {}


def create_default_values(key):
    cache_store[key] = {"default": True}


def parse_json(data):
    import json

    return json.loads(data) if isinstance(data, str) else data


def is_valid(data):
    return bool(data)


def execute_business_logic(data):
    return {"status": "success", "data": data}


def format_json_response(result):
    import json

    return json.dumps(result)


def error_response(message):
    return {"error": message}


def log_request(data):
    print(f"Logging request: {data}")


# =============================================================================
# Key Takeaways
# =============================================================================

"""
REFACTORING PATTERNS:

1. **Vague to Specific**
   - Before: process(), handle(), manage()
   - After: register_user(), process_api_request()
   - Use specific verbs that match actions

2. **Mixed to Separated**
   - Before: One function doing read + write
   - After: Separate functions for each concern
   - Compose with orchestrator if needed

3. **Surprising to Expected**
   - Before: get() that modifies, check() that creates
   - After: Honest names that match behavior
   - No hidden side effects

4. **Overgrown to Focused**
   - Before: Function grew beyond original name
   - After: Each function has single responsibility
   - Pipeline approach for multi-step operations

5. **Generic to Honest**
   - Before: Generic 'handle' or 'process'
   - After: Either specific or explicitly multi-step
   - Name communicates intent clearly

HARMONIZER AS REFACTORING GUIDE:

✅ Run Harmonizer before refactoring
   - Identifies disharmonious functions
   - Prioritizes by severity

✅ Run Harmonizer after refactoring
   - Verify improvements
   - Confirm semantic alignment

✅ Use scores as metrics
   - Track improvement over time
   - Set team standards (e.g., < 0.5)

✅ Focus on highest scores first
   - Critical (0.8+) → Immediate attention
   - High (0.5-0.8) → Next refactoring session
   - Low (< 0.5) → Monitor

BEFORE YOU REFACTOR:

1. Understand what function actually does
2. Identify semantic contradiction
3. Decide: Rename or refactor?
4. If refactoring: Separate concerns
5. Choose honest, descriptive names
6. Verify with Harmonizer

MEASURE SUCCESS:

    # Before refactoring
    harmonizer myfile.py > before.txt

    # After refactoring
    harmonizer myfile.py > after.txt

    # Compare scores - should decrease!

The goal: Code that says what it means and means what it says! 💛⚓
"""

# =============================================================================
# Run This Example
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("REFACTORING JOURNEY DEMO")
    print("=" * 70)
    print("\nThis file shows before/after refactoring examples.")
    print("\nRun: harmonizer examples/refactoring_journey.py")
    print("\nNotice:")
    print("  - 'BEFORE' functions have higher scores")
    print("  - 'AFTER' functions have lower scores")
    print("  - Score improvement shows semantic alignment")
    print("\nKey insight: Good refactoring reduces semantic distance!")
    print("=" * 70 + "\n")
