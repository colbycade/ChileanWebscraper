# Utility functions

import re

def parse_upload_desc(upload_desc):
    match = re.search(r"Enviado por (.+?) (\d+) (\w+) ago\. votos (-?\d+)", upload_desc)
    if not match:
        print('failed:', upload_desc)
        return '1','1',1
    user = match.group(1).strip()
    display_time = match.group(2) + ' ' + match.group(3)
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
    else:
        print(user, time_quantity, time_unit, votes, 'failed:', upload_desc)
        time_in_days = None  # This should not happen with the given pattern
    return user, display_time, time_in_days, votes

def print_def_data(entry_name:str, definition_data:dict):
    buffer = '\n                     '
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
        print(f'  Uploaded:        {definition_data["display_time"]} ago.')
        print(f'  # of Votes:      {definition_data["votes"]}')