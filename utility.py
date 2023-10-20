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
    if time_unit == 'year' or 'years':
        time_in_days = time_quantity * 365
    elif time_unit == 'month' or 'months':
        time_in_days = time_quantity * 30
    elif time_unit == 'week' or 'weeks':
        time_in_days = time_quantity * 7
    elif time_unit == 'day' or 'days':
        time_in_days = time_quantity
    else:
        print(user, time_quantity, time_unit, votes, 'failed:', upload_desc)
        time_in_days = None  # This should not happen with the given pattern
    return user, display_time, time_in_days, votes
