# Python Code Harmonizer - Tutorial

## Welcome!

This tutorial will walk you through using Python Code Harmonizer with real examples. By the end, you'll understand how to identify semantic bugs and improve your code's clarity.

---

## Table of Contents

1. [Setup](#setup)
2. [Tutorial 1: Your First Analysis](#tutorial-1-your-first-analysis)
3. [Tutorial 2: Understanding Disharmony Patterns](#tutorial-2-understanding-disharmony-patterns)
4. [Tutorial 3: Refactoring for Harmony](#tutorial-3-refactoring-for-harmony)
5. [Tutorial 4: Real-World Scenarios](#tutorial-4-real-world-scenarios)
6. [Tutorial 5: Building Good Habits](#tutorial-5-building-good-habits)
7. [Exercises](#exercises)

---

## Setup

**Before starting, ensure you have:**
```bash
# Install Python Code Harmonizer
pip install .

# Verify installation
harmonizer --help
```

**Create a practice directory:**
```bash
mkdir harmony-tutorial
cd harmony-tutorial
```

---

## Tutorial 1: Your First Analysis

### Step 1: Create a Simple File

Create `simple_example.py`:

```python
def get_user_data(user_id):
    """Retrieve user information from database"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    return user

def calculate_price(items):
    """Calculate total price of items"""
    total = sum(item.price for item in items)
    return total

def remove_user(user_id):
    """Delete user from database"""
    database.execute("DELETE FROM users WHERE id = ?", user_id)
    return True
```

### Step 2: Run the Harmonizer

```bash
harmonizer simple_example.py
```

### Step 3: Observe the Output

```
======================================================================
Python Code Harmonizer (v1.1) ONLINE
...
======================================================================

Analyzing file: simple_example.py
----------------------------------------------------------------------
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
get_user_data                | ✓ HARMONIOUS
calculate_price              | ✓ HARMONIOUS
remove_user                  | ✓ HARMONIOUS
======================================================================
Analysis Complete.
```

### What Just Happened?

**All three functions are HARMONIOUS** because:

1. **`get_user_data`**:
   - Name says: "get" (retrieve information)
   - Code does: `query` (retrieve information)
   - ✓ ALIGNED

2. **`calculate_price`**:
   - Name says: "calculate" (compute a value)
   - Code does: `sum` (compute a value)
   - ✓ ALIGNED

3. **`remove_user`**:
   - Name says: "remove" (delete/destroy)
   - Code does: `DELETE` (delete/destroy)
   - ✓ ALIGNED

**Key Learning:** When function names match their implementation's semantic meaning, harmony scores stay low.

---

## Tutorial 2: Understanding Disharmony Patterns

Now let's introduce semantic bugs and see how Harmonizer catches them.

### Pattern 1: Action Contradiction

Create `contradictions.py`:

```python
def get_user_data(user_id):
    """Retrieve user information"""
    # BUG: Says "get" but actually "delete"!
    database.execute("DELETE FROM users WHERE id = ?", user_id)
    return None

def validate_email(email):
    """Check if email is valid format"""
    # BUG: Says "validate" but actually "send"!
    email_service.send_welcome_email(email)
    return True

def check_permissions(user):
    """Verify user has required permissions"""
    # BUG: Says "check" but actually "modify"!
    user.permissions = "admin"
    database.save(user)
    return True
```

Run the harmonizer:

```bash
harmonizer contradictions.py
```

**Expected Output:**

```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
get_user_data                | !! DISHARMONY (Score: 1.41)
validate_email               | !! DISHARMONY (Score: 0.95)
check_permissions            | !! DISHARMONY (Score: 0.78)
```

### Why These Score High:

1. **`get_user_data` (Score: 1.41 - CRITICAL)**
   - Intent: "get" = retrieve, read (Wisdom domain)
   - Execution: "delete" = destroy, force (Power domain)
   - These are **semantic opposites** → Very high score

2. **`validate_email` (Score: 0.95 - HIGH)**
   - Intent: "validate" = check, verify (Justice domain)
   - Execution: "send" = action, transmission (Power domain)
   - Checking vs. acting → Significant mismatch

3. **`check_permissions` (Score: 0.78 - HIGH)**
   - Intent: "check" = read-only verification (Justice/Wisdom)
   - Execution: "modify" = state change (Power)
   - Read vs. write → Clear violation

### Pattern 2: Scope Mismatch

Create `scope_mismatch.py`:

```python
def delete_user_session(session_id):
    """Remove user's current session"""
    # BUG: Deletes entire user, not just session!
    database.execute("DELETE FROM users WHERE session_id = ?", session_id)
    database.execute("DELETE FROM sessions WHERE id = ?", session_id)

def update_username(user_id, new_name):
    """Change user's username"""
    # BUG: Updates more than just username!
    database.execute("""
        UPDATE users
        SET username = ?,
            email = ?,
            permissions = 'admin',
            last_modified = NOW()
        WHERE id = ?
    """, new_name, "admin@example.com", user_id)
```

Run harmonizer:

```bash
harmonizer scope_mismatch.py
```

**Why These Score High:**

- Function promises specific scope but delivers broader scope
- `delete_user_session` says "session" but deletes "user" → Semantic overreach
- `update_username` says "username" but changes email, permissions, etc. → Scope violation

### Pattern 3: Vague Names with Specific Actions

Create `vague_names.py`:

```python
def process_data(data):
    """Process incoming data"""
    # What does "process" mean? This is TOO specific for such a vague name
    database.execute("DELETE FROM archive WHERE data_id = ?", data.id)

def handle_request(request):
    """Handle incoming request"""
    # "Handle" is vague, but this does something very specific
    user_service.permanently_ban_user(request.user_id)

def manage_user(user_id):
    """Manage user account"""
    # "Manage" is vague, this is destructive
    database.execute("DROP TABLE users")
```

**Why These May Show Moderate Disharmony:**

- Vague verbs ("process", "handle", "manage") paired with specific, powerful actions
- Creates semantic ambiguity
- Scores may be moderate (0.4-0.7) depending on specific implementation

---

## Tutorial 3: Refactoring for Harmony

Let's take disharmonious code and fix it.

### Example: The "get_user" Bug

**BEFORE (Disharmonious):**

```python
def get_user(user_id):
    """Retrieve user by ID"""
    database.execute("DELETE FROM users WHERE id = ?", user_id)
    return None
```

**Harmonizer says:** `!! DISHARMONY (Score: 1.41)`

### Fix Option 1: Correct the Implementation

If the name is right but code is wrong:

```python
def get_user(user_id):
    """Retrieve user by ID"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    return user
```

**Harmonizer says:** `✓ HARMONIOUS`

### Fix Option 2: Correct the Name

If the code is right but name is wrong:

```python
def delete_user(user_id):
    """Remove user from system"""
    database.execute("DELETE FROM users WHERE id = ?", user_id)
    return None
```

**Harmonizer says:** `✓ HARMONIOUS`

### Fix Option 3: Split the Function

If it legitimately does both:

```python
def get_and_archive_user(user_id):
    """Retrieve user data and move to archive (deletes from active users)"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    database.execute("INSERT INTO archived_users SELECT * FROM users WHERE id = ?", user_id)
    database.execute("DELETE FROM users WHERE id = ?", user_id)
    return user
```

**Note:** This might still show slight disharmony (mixed semantics), which is OK if intentional and documented.

### Practice Exercise

**Fix this code:**

```python
def validate_and_send_email(email):
    """Check email format and send welcome message"""
    if "@" not in email:
        return False
    email_service.send(email, "Welcome!")
    return True
```

**Refactoring options:**

**Option A: Split into two functions**
```python
def validate_email(email):
    """Check if email format is valid"""
    return "@" in email

def send_welcome_email(email):
    """Send welcome message to email"""
    email_service.send(email, "Welcome!")
    return True

# Usage
if validate_email(user.email):
    send_welcome_email(user.email)
```

**Option B: Rename to match dual purpose**
```python
def validate_and_send_welcome_email(email):
    """Validate email format, then send welcome message if valid"""
    if "@" not in email:
        return False
    email_service.send(email, "Welcome!")
    return True
```

**Which is better?**
- **Option A** = Better separation of concerns, more testable, more reusable
- **Option B** = Acceptable if this specific sequence is always needed together

---

## Tutorial 4: Real-World Scenarios

### Scenario 1: Code Review

You're reviewing a pull request. Run harmonizer:

```bash
harmonizer pr_branch/new_feature.py
```

**Output:**
```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
authenticate_user            | !! DISHARMONY (Score: 0.92)
fetch_data                   | ✓ HARMONIOUS
save_results                 | ✓ HARMONIOUS
```

**Investigation:**

```python
def authenticate_user(username, password):
    """Verify user credentials"""
    if check_password(username, password):
        # BUG: Authentication function is creating sessions!
        session = create_new_session(username)
        grant_admin_privileges(username)  # BUG: And granting admin!
        return session
    return None
```

**Problem:** Function promises authentication (verification) but also performs authorization actions (granting privileges).

**Fix:**
```python
def authenticate_user(username, password):
    """Verify user credentials and return user object if valid"""
    if check_password(username, password):
        return get_user(username)
    return None

def create_user_session(user):
    """Create new session for authenticated user"""
    return create_new_session(user.username)
```

### Scenario 2: Legacy Code Cleanup

You're refactoring old code. Run harmonizer on legacy module:

```bash
harmonizer legacy/user_management.py
```

**Output:**
```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
process_user                 | !! DISHARMONY (Score: 1.15)
handle_data                  | !! DISHARMONY (Score: 0.89)
do_stuff                     | !! DISHARMONY (Score: 0.76)
user_function                | !! DISHARMONY (Score: 0.65)
```

**Analysis:** All functions have vague names. Let's look at one:

```python
def process_user(user_id):
    """Process user"""
    # What does this actually do?
    database.execute("DELETE FROM temp_users WHERE id = ?", user_id)
    database.execute("INSERT INTO permanent_users SELECT * FROM users WHERE id = ?", user_id)
    send_confirmation_email(user_id)
    log_event("user_activated", user_id)
```

**Better name:**
```python
def activate_user_account(user_id):
    """Activate user by moving from temporary to permanent storage"""
    database.execute("DELETE FROM temp_users WHERE id = ?", user_id)
    database.execute("INSERT INTO permanent_users SELECT * FROM users WHERE id = ?", user_id)
    send_confirmation_email(user_id)
    log_event("user_activated", user_id)
```

**Key insight:** Vague names like "process", "handle", "do_stuff", "function" are code smells that harmonizer catches.

### Scenario 3: API Design

You're designing a public API. Run harmonizer:

```bash
harmonizer api/endpoints.py
```

**Output:**
```
FUNCTION NAME                | INTENT-EXECUTION DISHARMONY
-----------------------------|--------------------------------
get_user                     | !! DISHARMONY (Score: 0.71)
```

**Investigation:**
```python
@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /api/users/:id - Retrieve user information"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)

    # BUG: GET endpoint is modifying state!
    database.execute("UPDATE users SET last_accessed = NOW() WHERE id = ?", user_id)
    analytics.track_access(user_id)

    return jsonify(user)
```

**Problem:** GET requests should be read-only (REST principle), but this modifies database.

**Fix Option 1: Make it truly read-only**
```python
@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /api/users/:id - Retrieve user information"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    # Track access asynchronously without blocking/modifying
    analytics_queue.add("user_accessed", user_id)
    return jsonify(user)
```

**Fix Option 2: Use POST if modification is essential**
```python
@app.route("/api/users/<user_id>/access", methods=["POST"])
def record_user_access(user_id):
    """POST /api/users/:id/access - Record access and return user data"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    database.execute("UPDATE users SET last_accessed = NOW() WHERE id = ?", user_id)
    analytics.track_access(user_id)
    return jsonify(user)
```

---

## Tutorial 5: Building Good Habits

### Habit 1: Name Functions After What They DO

**Bad:**
```python
def user_function(user):  # What does this do?
def handle_user(user):    # Handle how?
def process_data(data):   # Process how?
```

**Good:**
```python
def delete_inactive_user(user)
def send_welcome_email_to_user(user)
def archive_user_data(data)
```

### Habit 2: Use Semantic Verb Patterns

**Reading Operations** (Wisdom domain):
- `get_*`, `fetch_*`, `retrieve_*`, `find_*`, `query_*`, `read_*`

**Validation Operations** (Justice domain):
- `validate_*`, `verify_*`, `check_*`, `is_*`, `has_*`

**Writing Operations** (Power domain):
- `create_*`, `update_*`, `delete_*`, `remove_*`, `insert_*`, `save_*`

**Computation Operations** (Wisdom domain):
- `calculate_*`, `compute_*`, `analyze_*`, `transform_*`

**Mixed Operations** (Be explicit):
- `get_or_create_*`, `find_and_update_*`, `validate_and_save_*`

### Habit 3: Run Harmonizer on New Code

**Before committing:**
```bash
git diff --name-only | grep '\.py$' | xargs harmonizer
```

**Before pushing:**
```bash
harmonizer $(git diff origin/main --name-only | grep '\.py$')
```

### Habit 4: Set Team Standards

**Example team policy:**
- ✅ All functions must score < 0.5 (harmonious)
- ⚠️ Functions 0.5-0.8 require explanation in PR
- ❌ Functions > 0.8 must be refactored

---

## Exercises

### Exercise 1: Identify the Bug

What's wrong with this code? Run harmonizer to verify your intuition.

```python
def backup_database():
    """Create backup of database"""
    database.execute("DROP DATABASE production")
```

<details>
<summary>Answer</summary>

**Problem:** Function says "backup" (preservation) but does "DROP" (destruction)

**Fix:**
```python
def backup_database():
    """Create backup of database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    database.execute(f"CREATE DATABASE backup_{timestamp} AS COPY OF production")
```
</details>

### Exercise 2: Refactor for Harmony

Refactor this function to reduce disharmony:

```python
def get_user_profile(user_id):
    """Retrieve user profile information"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    user.last_login = datetime.now()
    database.save(user)
    send_analytics_event("profile_viewed", user_id)
    return user
```

<details>
<summary>Solution</summary>

**Option A: Make it truly read-only**
```python
def get_user_profile(user_id):
    """Retrieve user profile information (read-only)"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    return user

def record_profile_view(user_id):
    """Record that user profile was viewed"""
    user = get_user_profile(user_id)
    user.last_login = datetime.now()
    database.save(user)
    send_analytics_event("profile_viewed", user_id)
```

**Option B: Rename to match behavior**
```python
def get_user_profile_and_record_access(user_id):
    """Retrieve user profile and record access time"""
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    user.last_login = datetime.now()
    database.save(user)
    send_analytics_event("profile_viewed", user_id)
    return user
```
</details>

### Exercise 3: Design Good Names

You need functions that:
1. Check if email format is valid
2. Send email to user
3. Check email validity AND send if valid
4. Delete user's email from database
5. Update user's email address

Write good function names and verify with harmonizer.

<details>
<summary>Solution</summary>

```python
def validate_email_format(email):
    """Check if email string has valid format"""
    return "@" in email and "." in email

def send_email(to_address, subject, body):
    """Send email message to address"""
    email_service.send(to_address, subject, body)

def validate_and_send_email(email, subject, body):
    """Validate email format and send message if valid"""
    if validate_email_format(email):
        send_email(email, subject, body)
        return True
    return False

def delete_user_email(user_id):
    """Remove user's email address from database"""
    database.execute("UPDATE users SET email = NULL WHERE id = ?", user_id)

def update_user_email(user_id, new_email):
    """Change user's email address"""
    database.execute("UPDATE users SET email = ? WHERE id = ?", new_email, user_id)
```

All should show low disharmony scores!
</details>

---

## Next Steps

**You've completed the tutorial!** You now understand:

✅ How to run Python Code Harmonizer
✅ How to interpret disharmony scores
✅ Common patterns that cause semantic bugs
✅ How to refactor code for harmony
✅ How to build good naming habits

**Continue learning:**
- Read the [User Guide](USER_GUIDE.md) for comprehensive usage info
- Explore the [Philosophy](PHILOSOPHY.md) to understand the Anchor Point and ICE Framework
- Check the [FAQ](FAQ.md) for common questions

**Practice makes perfect:**
- Run harmonizer on your own code
- Make it part of your daily workflow
- Share findings with your team

---

**Happy coding, and may your functions always do what their names promise!** 💛⚓
