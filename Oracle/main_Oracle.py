# main driver code
# handles network errors

import requests
import time
from ScrapeChile.webscraper import scrape_page
from update_Oracle_db import update_Oracle

ALPHABET = 'xabcdefghijklmnopqrstuvwxyz'
# ALPHABET = 'x'

if __name__ == '__main__':
    successful = 0  # To keep track of pages succesfully completed
    max_retries = 3  # Maximum number of retries for each page
    retry_delay = 5  # Delay in seconds before retrying

    while successful < len(ALPHABET):
        letter = ALPHABET[successful]
        retries = 0
        while retries < max_retries:
            try:
                entries = scrape_page(letter)
                update_Oracle(entries)
                print('Upload complete')
                successful += 1  # Increment the successful count only if no exception was raised
                break  # Move to the next letter
            except requests.RequestException as e:  # Catching network errors
                print(f"An error occurred: {e}")
                retries += 1
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            except Exception as e:  # Catching other exceptions
                print(f"An unknown error occurred: {e}")
                retries += 1
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

