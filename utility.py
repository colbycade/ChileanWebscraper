# Utility functions

import re
import hashlib

def parse_upload_desc(upload_desc):
    match = re.search(r"Enviado por (.+?) (\d+) (\w+) ago\. votos (-?\d+)", upload_desc)
    if not match:
        print('failed:', upload_desc)
        return '1','1',1
    user = match.group(1).strip()
    time_since_upload = match.group(2) + ' ' + match.group(3)
    time_quantity = int(match.group(2))
    time_unit = match.group(3)
    votes = int(match.group(4))

    # Convert time_quantity to days
    if time_unit == 'year' or time_unit == 'years':
        time_in_days = time_quantity * 365
    elif time_unit == 'month' or time_unit == 'months':
        time_in_days = time_quantity * 30
    elif time_unit == 'week' or time_unit == 'weeks':
        time_in_days = time_quantity * 7
    elif time_unit == 'day' or time_unit == 'days':
        time_in_days = time_quantity
    elif time_unit == 'hour' or time_unit == 'hours':
        time_in_days = round(time_quantity / 24, 2)
    elif time_unit == 'minute' or time_unit == 'minutes':
        time_in_days = round(time_quantity / (24*60), 2)
    elif time_unit == 'second' or time_unit == 'seconds':
        time_in_days = round(time_quantity / (24*3600), 2)
    else:
        print(user, time_quantity, time_unit, votes, 'failed:', upload_desc)
        time_in_days = -1  # This should not happen with the given pattern
    return user, time_since_upload, time_in_days, votes

def print_def_data(entries):
    buffer = '\n                     '
    for entry_name, definitions in entries.items():
        for definition_data in definitions:
            print()
            print(f'Entry: {entry_name}')
            for i in range(1, len(definition_data)+1):
                print(f'Definition {i} for "{entry_name}":')
                indented_definition = buffer.join(definition_data["definition_text"].split('\n'))
                print(f'  Definition Text: [{buffer}{indented_definition}{buffer[:-2]}]')
                indented_examples = buffer.join(definition_data["example_text"].split('\n'))
                print(f'  Example Text:    [{buffer}{indented_examples}{buffer[:-2]}]')
                synonyms_str = ", ".join([f'"{s}"' for s in definition_data["synonyms"]]) if definition_data[
                    "synonyms"] else "None"
                print(f'  Synonyms:        {synonyms_str}')
                print(f'  User:            {definition_data["username"]}')
                print(f'  Uploaded:        {definition_data["time_since_upload"]} ago.')
                print(f'  # of Votes:      {definition_data["votes"]}')

def calculate_hash(definition_data, entry_id, user_id):
    m = hashlib.sha256()
    concatenated_data = f"{definition_data['definition_text']}{entry_id}{user_id}"
    m.update(concatenated_data.encode('utf-8'))
    return m.hexdigest()
