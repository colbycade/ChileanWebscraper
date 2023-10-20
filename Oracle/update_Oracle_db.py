# Function to update Oracle database tables

import oracledb


def update_Oracle(entry_name, definition_data):
    conn = oracledb.connect(
        user="WORKFLOW",
        password="VivaChile123",
        dsn="scrapechile_low",
        config_dir="Config",
        wallet_location="Config",
        wallet_password="VivaChile123")

    cursor = conn.cursor()

    # Update "users" table if user is new
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = :username", username=definition_data['username'])
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username) VALUES (:username)", username=definition_data['username'])

    # Update "entries" table if entry is new
    cursor.execute("SELECT COUNT(*) FROM entries WHERE entry_name = :entry_name", entry_name=entry_name)
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO entries (entry_name) VALUES (:entry_name)", entry_name=entry_name)

    # Get foreign keys for "definitions" table
    cursor.execute("SELECT user_id FROM users WHERE username = :username", username=definition_data['username'])
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT entry_id FROM entries WHERE entry_name = :entry_name", entry_name=entry_name)
    entry_id = cursor.fetchone()[0]

    # Update "definitions" table
    cursor.execute("""
    INSERT INTO definitions 
    (definition_text, example_text, synonyms, time_since_upload, time_in_days, votes, entry_id, user_id)
    VALUES (:definition_text, :example_text, :synonyms, :display_time, :time_in_days, :votes, :entry_id, :user_id)
    """, {
        'definition_text': definition_data['definition_text'],
        'example_text': definition_data['example_text'],
        'synonyms': ', '.join(definition_data['synonyms']),
        'display_time': definition_data['time_since_upload'],
        'time_in_days': definition_data['time_in_days'],
        'votes': definition_data['votes'],
        'entry_id': entry_id,
        'user_id': user_id,
    })

    conn.commit()
    cursor.close()
    conn.close()