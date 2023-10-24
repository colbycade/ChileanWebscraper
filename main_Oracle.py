# main driver code for updating Oracle DB
# handles network errors
import requests
import time
from webscraper import scrape_page
from batchinsert import update_oracle_db

if __name__ == '__main__':
    successful = 0  # To keep track of pages succesfully completed
    max_retries = 3  # Maximum number of retries for each page
    retry_delay = 5  # Delay in seconds before retrying

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    while successful < len(ALPHABET):
        letter = ALPHABET[successful]
        retries = 0
        while retries < max_retries:
            try:
                entries = scrape_page(letter)
                update_oracle_db(entries)
                print(f'Upload of new data for letter "{letter}" complete')
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
