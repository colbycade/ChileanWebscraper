import mysql.connector
def update_database(entry_name, definition_data):
    conn = mysql.connector.connect(user='root', password='vivachile',
                                   host='localhost', database='ScrapeChile')
    cursor = conn.cursor()

    # Update "users" table
    cursor.execute("INSERT IGNORE INTO users (username) VALUES (%s)", (definition_data['username'],))

    # Update "entries" table
    cursor.execute("INSERT IGNORE INTO entries (entry_name) VALUES (%s)", (entry_name,))

    # Get foreign keys for "definitions" table
    cursor.execute("SELECT user_id FROM users WHERE username = %s", (definition_data['username'],))
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT entry_id FROM entries WHERE entry_name = %s", (entry_name,))
    entry_id = cursor.fetchone()[0]

    # Update "definitions" table
    cursor.execute("""
    INSERT INTO definitions (definition_text, example_text, 
    synonyms, display_time, time_in_days, votes, entry_id, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
          definition_data['definition_text'],
          definition_data['example_text'],
          ', '.join(definition_data['synonyms']),
          definition_data['display_time'],
          definition_data['time_in_days'],
          definition_data['votes'],
          entry_id,
          user_id,
        )
    )

    conn.commit()
    cursor.close()
    conn.close()
