# Function to update Oracle database tables using batch inserts

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

    # Pre-fetch existing user_ids and entry_ids
    username_to_id = {row[0]: row[1] for row in cursor.execute("SELECT username, user_id FROM users")}
    entryname_to_id = {row[0]: row[1] for row in cursor.execute("SELECT entry_name, entry_id FROM entries")}

    user_batch = []
    entry_batch = []
    definition_batch = []

    for entry_name, definitions in tqdm(entries.items(), desc="Updating users and entries...", unit="updates", leave=False):
        for definition_data in definitions:
            username = definition_data['username']

            # Prepare batch of new user ids
            user_id = username_to_id.get(username)
            if user_id is None:
                user_batch.append({'username': username})
                # username_to_id.update({'username': username})

            # Prepare batch of new entry ids
            entry_id = entryname_to_id.get(entry_name)
            if entry_id is None:
                entry_batch.append({'entry_name': entry_name})
    print(user_batch)
    print(entry_batch)

    # Execute batch ID inserts and populate the ID dictionaries
    if user_batch:
        cursor.executemany("""
        INSERT INTO users (username)
        SELECT :username FROM dual
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = :username)
        """, user_batch)
        new_user_ids = cursor.execute("SELECT username, user_id FROM users WHERE username IN (:usernames)", {'usernames': d['username'] for d in user_batch})

        # Update the existing username_to_id dictionary with new user_ids
        for username, user_id in new_user_ids:
            username_to_id[username] = user_id
        # username_to_id.update(new_user_ids)
    else:
        print("No new users")

    if entry_batch:
        cursor.executemany("""
        INSERT INTO entries (entry_name)
        SELECT :entry_name FROM dual
        WHERE NOT EXISTS (SELECT 1 FROM entries WHERE entry_name = :entry_name)
        """, entry_batch)
        new_entry_ids = cursor.execute("SELECT entry_name, entry_id FROM entries WHERE entry_name IN (:entry_names)", {'entry_names': [d['entry_name'] for d in entry_batch]})
        entryname_to_id.update(new_entry_ids)
    else:
        print("No new entries")

    # Prepare batch for definitions
    for entry_name, definitions in tqdm(entries.items(), desc="Preparing definitions for insertion...", unit=" definitions", leave=False):
        for definition_data in definitions:
            username = definition_data['username']
            user_id = username_to_id.get(username)
            entry_id = entryname_to_id.get(entry_name)

            if user_id and entry_id:
                definition_hash = calculate_hash(definition_data, entry_id, user_id)
                # Prepare data for batch insertion for "definitions" table
                definition_batch.append({
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
            else:
                raise ValueError("No user and/or entry id found")

    # Execute batch insert for definitions
    cursor.executemany("""
    INSERT INTO definitions (definition_id, definition_text, example_text,
    synonyms, time_since_upload, time_in_days, votes, entry_id, user_id)
    SELECT :definition_id, :definition_text, :example_text, :synonyms,
    :time_since_upload, :time_in_days, :votes, :entry_id, :user_id FROM dual
    WHERE NOT EXISTS (SELECT 1 FROM definitions WHERE definition_id = :definition_id)
    """, definition_batch)

    conn.commit()
    cursor.close()
    conn.close()
