# Function to update Oracle database tables using batch inserts

import oracledb
from tqdm import tqdm
from utility import calculate_hash


def update_oracle_db(entries:dict) -> None:
    conn = oracledb.connect(
        user="WORKFLOW",
        password="VivaChile123",
        dsn="scrapechile_low",
        config_dir="Oracle_config",
        wallet_location="Oracle_config",
        wallet_password="VivaChile123")

    cursor = conn.cursor()

    # Pre-fetch existing users and entries
    usernames = {row[0] for row in cursor.execute("SELECT username FROM users")}
    entry_names = {row[0] for row in cursor.execute("SELECT entry_name FROM entries")}
    definitions_hashes = {row[0] for row in cursor.execute("SELECT definition_id FROM definitions")}

    user_batch = []
    entry_batch = []
    definition_batch = []

    for entry_name, definitions in tqdm(entries.items(), desc="Preparing data for upload", unit="updates", leave=False):
        for definition_data in definitions:
            username = definition_data['username']

            # Prepare batch of new users
            if username not in usernames:
                user_batch.append({'username': username})

            # Prepare batch of new entries
            if entry_name not in entry_names:
                entry_batch.append({'entry_name': entry_name})

            # Prepare batch of new definitions
            definition_hash = calculate_hash(definition_data, entry_name, username)
            if definition_hash not in definitions_hashes:
                definition_batch.append({
                    'definition_id': definition_hash,
                    'definition_text': definition_data['definition_text'],
                    'example_text': definition_data['example_text'],
                    'synonyms': ', '.join(definition_data['synonyms']),
                    'time_since_upload': definition_data['time_since_upload'],
                    'time_in_days': definition_data['time_in_days'],
                    'votes': definition_data['votes'],
                    'entry_name': entry_name,
                    'username': username,
                })

    # Execute batch inserts
    if user_batch:
        cursor.executemany("""
        INSERT INTO users (username)
        SELECT :username FROM dual
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = :username)
        """, user_batch)
    else:
        print("No new users")

    if entry_batch:
        cursor.executemany("""
        INSERT INTO entries (entry_name)
        SELECT :entry_name FROM dual
        WHERE NOT EXISTS (SELECT 1 FROM entries WHERE entry_name = :entry_name)
        """, entry_batch)
    else:
        print("No new entries")

    if definition_batch:
        cursor.executemany("""
        INSERT INTO definitions (definition_id, definition_text, example_text,
        synonyms, time_since_upload, time_in_days, votes, entry_name, username)
        SELECT :definition_id, :definition_text, :example_text, :synonyms,
        :time_since_upload, :time_in_days, :votes, :entry_name, :username FROM dual
        WHERE NOT EXISTS (SELECT 1 FROM definitions WHERE definition_id = :definition_id)
        """, definition_batch)
    else:
        print("No new definitions")

    conn.commit()
    cursor.close()
    conn.close()

    return None
