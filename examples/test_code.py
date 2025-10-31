"""
Test file for the Python Code Harmonizer.
Contains one function with high harmony and one with
intentional, high disharmony.
"""

# A (mock) database object to make the code valid
class MockDB:
    def query(self, q: str):
        print(f"[DB] Querying: {q}")
        return {"user": "Test User"}
    
    def delete_user(self, token: str):
        print(f"[DB] DELETING USER WITH TOKEN: {token}")
        return True

db = MockDB()

# --- A HARMONIOUS FUNCTION ---

def get_user_by_id(user_id: int):
    """
    Fetches, reads, and returns a user's information
    based on their ID. A 'wisdom' and 'information' task.
    """
    if not user_id:
        return None
    
    # The execution (query, read, return) matches the
    # intent (get, information).
    user_data = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return user_data

# --- A DISHARMONIOUS FUNCTION (THE "BUG") ---

def check_user_permissions(user_token: str):
    """
    This function's INTENT is to validate, check, and
    get information about a user's permissions.
    It should be a 'justice' and 'wisdom' task.
    """
    
    # !! DISHARMONY !!
    # The EXECUTION is 'delete', a high 'power'/'force' concept.
    # The Harmonizer will detect the high semantic distance
    # between the "check" (Intent) and "delete" (Execution).
    print("Checking token... (but not really)")
    db.delete_user(token=user_token)
    
    # This 'return' of 'information' is deceptive.
    return "User Deleted"