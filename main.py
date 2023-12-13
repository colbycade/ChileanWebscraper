# main driver code
# handles network errors

import requests
import time
from update_MySQL import update_mysql_db
from webscraper import scrape_page
from utility import print_def_data

if __name__ == '__main__':
    # # If you want to print out entries instead of updating database, uncomment this and comment out the rest:
    #     entries = scrape_page(letter)
    #     print_def_data(entries)

    successful = 0  # To keep track of pages succesfully completed
    max_retries = 3  # Maximum number of retries for each page
    retry_delay = 5  # Delay in seconds before retrying

    # for letter in ALPHABET:  # replace ALPHABET with specific page/letter if desired
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    while successful < len(ALPHABET):
        letter = ALPHABET[successful]
        retries = 0
        while retries < max_retries:
            try:
                entries = scrape_page(letter)
                update_mysql_db(entries)
                print('Upload complete')
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
