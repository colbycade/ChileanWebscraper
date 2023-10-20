# main driver code
# handles network errors

import requests
from update_db import update_database
from webscraper import scrape_page
import time

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

if __name__ == '__main__':
    successful = 0  # To keep track of successful letters
    max_retries = 3  # Maximum number of retries for each letter
    retry_delay = 5  # Delay in seconds before retrying

    while successful < len(ALPHABET):
        letter = ALPHABET[successful]
        retries = 0
        while retries < max_retries:
            try:
                entries = scrape_page(letter)
                for entry_name, definitions in entries.items():
                    for definition_data in definitions:
                        update_database(entry_name, definition_data)
                successful += 1  # Increment the successful count only if no exception was raised
                break  # Move to the next letter
            except requests.RequestException as e:  # Catching network errors
                print(f"An error occurred: {e}")
                retries += 1
                print(f"Retrying {letter} in {retry_delay} seconds...")
                time.sleep(retry_delay)
            except Exception as e:  # Catching other exceptions
                print(f"An unknown error occurred: {e}")
                retries += 1
                print(f"Retrying {letter} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        # # Print:
        # buffer = '\n                     '
        # for entry_name, definitions in entries.items():
        #     print()
        #     print(f'Entry: {entry_name}')
        #     for i, definition_data in enumerate(definitions, start=1):
        #         print(f'Definition {i}:')
        #         indented_definition = buffer.join(definition_data["definition_text"].split('\n'))
        #         print(f'  Definition Text: [{buffer}{indented_definition}{buffer[:-2]}]')
        #         indented_examples = buffer.join(definition_data["example_text"].split('\n'))
        #         print(f'  Example Text:    [{buffer}{indented_examples}{buffer[:-2]}]')
        #         synonyms_str = ", ".join([f'"{s}"' for s in definition_data["synonyms"]]) if definition_data["synonyms"] else "None"
        #         print(f'  Synonyms:        {synonyms_str}')
        #         print(f'  User:            {definition_data["username"]}')
        #         print(f'  Uploaded:        {definition_data["time"]} ago.')
        #         print(f'  # of Votes:      {definition_data["votes"]}')
