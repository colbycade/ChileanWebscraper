# Function to update Oracle database tables

import oracledb
from tqdm import tqdm
from utility import calculate_hash


def update_oracle_db(entries):
    conn = oracledb.connect(
        user="WORKFLOW",
        password="VivaChile123",
        dsn="scrapechile_low",
        config_dir="Oracle_config",
        wallet_location="Oracle_config",
        wallet_password="VivaChile123")

    cursor = conn.cursor()

    for entry_name, definitions in tqdm(entries.items(), desc="Updating database...", unit="updates", leave=False):
        for definition_data in definitions:
            # Update "users" table if user is new
            username = definition_data['username']
            cursor.execute("""
            INSERT INTO users (username)
            SELECT :username FROM dual
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = :username)
            """, {'username': username})

            cursor.execute("SELECT user_id FROM users WHERE username = :username", {'username': username})
            user_id = cursor.fetchone()[0]

            # Update "entries" table if entry is new
            cursor.execute("""
            INSERT INTO entries (entry_name)
            SELECT :entry_name FROM dual
            WHERE NOT EXISTS (SELECT 1 FROM entries WHERE entry_name = :entry_name)
            """, {'entry_name': entry_name})

            cursor.execute("SELECT entry_id FROM entries WHERE entry_name = :entry_name", {'entry_name': entry_name})
            entry_id = cursor.fetchone()[0]

            # Calculate unique has for defintion based on user, entry, and definition given (we technically lose
            # information if the same user uploads the same definition twice but that's fine for our purposes)
            definition_hash = calculate_hash(definition_data, entry_id, user_id)

            # Update "definitions" table if new
            cursor.execute("""
            INSERT INTO definitions (definition_id, definition_text, example_text, 
            synonyms, time_since_upload, time_in_days, votes, entry_id, user_id)
            SELECT :definition_id, :definition_text, :example_text, :synonyms, 
            :time_since_upload, :time_in_days, :votes, :entry_id, :user_id FROM dual
            WHERE NOT EXISTS (SELECT 1 FROM definitions WHERE definition_id = :definition_id)
            """, {
                'definition_id': definition_hash,
                'definition_text': definition_data['definition_text'],
                'example_text': definition_data['example_text'],
                'synonyms': ', '.join(definition_data['synonyms']),
                'time_since_upload': definition_data['time_since_upload'],
                'time_in_days': definition_data['time_in_days'],
                'votes': definition_data['votes'],
                'entry_id': entry_id,
                'user_id': user_id,
            })

    conn.commit()
    cursor.close()
    conn.close()