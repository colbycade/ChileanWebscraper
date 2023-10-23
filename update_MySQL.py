# Function to update database tables

import mysql.connector
from utility import calculate_hash
from tqdm import tqdm
def update_mysql_db(entries):
    conn = mysql.connector.connect(
        user='root',
        password='vivachile',
        host='localhost',
        database='ScrapeChile')

    cursor = conn.cursor()

    for entry_name, definitions in entries.items():
        for definition_data in definitions:
            # Update "users" table
            cursor.execute("INSERT IGNORE INTO users (username) VALUES (%s)", (definition_data['username'],))

            # Update "entries" table
            cursor.execute("INSERT IGNORE INTO entries (entry_name) VALUES (%s)", (entry_name,))

            # Get foreign keys for "definitions" table
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (definition_data['username'],))
            user_id = cursor.fetchone()[0]
            cursor.execute("SELECT entry_id FROM entries WHERE entry_name = %s", (entry_name,))
            entry_id = cursor.fetchone()[0]

            # Calculate unique has for defintion based on user, entry, and definition given (we technically lose
            # information if the same user uploads the same definition twice but that's fine for our purposes)
            definition_hash = calculate_hash(definition_data, entry_id, user_id)

            # Update "definitions" table if new
            cursor.execute("""
            INSERT IGNORE INTO definitions (definition_id, definition_text, example_text, 
            synonyms, time_since_upload, time_in_days, votes, entry_id, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                  definition_hash,
                  definition_data['definition_text'],
                  definition_data['example_text'],
                  ', '.join(definition_data['synonyms']),
                  definition_data['time_since_upload'],
                  definition_data['time_in_days'],
                  definition_data['votes'],
                  entry_id,
                  user_id,
                )
            )

    conn.commit()
    cursor.close()
    conn.close()
