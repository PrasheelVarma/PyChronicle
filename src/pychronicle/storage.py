import json

def insert_variable_state(conn, line_number, var_name, var_value):
    """
    Week 1: Safely serializes a Python variable and inserts it
    into the tracking database.
    """
    try:
        cursor = conn.cursor()

        # Serialize the value into a string so SQLite can store complex objects (like lists/dicts)
        serialized_val = json.dumps(var_value)

        # Insert the record into our table
        cursor.execute('''
            INSERT INTO variable_history (line_number, variable_name, serialized_value)
            VALUES (?, ?, ?)
        ''', (line_number, var_name, serialized_val))

        conn.commit()
        print(f"💾 Logged: {var_name} at line {line_number}")

    except Exception as e:
        print(f"❌ Failed to insert variable state: {e}")

# You can add a quick test at the bottom of the file:
if __name__ == "__main__":
    db = initialize_database()
    if db:
        # Simulating finding a variable x = [1, 2, 3] on line 10
        insert_variable_state(db, 10, "x", [1, 2, 3])
        db.close()
