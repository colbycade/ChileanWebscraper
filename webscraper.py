import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import re

BASE_URL = 'https://diccionariochileno.cl/terms/'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def scrape_diccionariochileno():
    all_entries = {}
    session = requests.Session()

    for letter in ALPHABET:
        url = f'{BASE_URL}{letter}'
        response = session.get(url)
        if response.status_code != 200:
            print(f'Failed to retrieve page for letter {letter}')
            # continue
        else:
            print(f'Page for letter "{letter}" retrieved')

        soup = BeautifulSoup(response.content, 'html.parser')
        entries_ul = soup.find('ul', class_='terms')
        entries_li = entries_ul.find_all('li') if entries_ul else []

        with tqdm(total=len(entries_li)+1, desc=f'Processing entries for {letter}', unit=' entries', leave=False) as pbar:
            for entry_li in entries_li:
                # Check if the li element has class 'title', and skip it
                if entry_li.get('class') and 'title' in entry_li['class']:
                    continue

                entry_name = re.sub(r'[\d\(\)\n\t]+', '', entry_li.text).strip().lower()  # Clean up the entry name
                href = entry_li.find('a')['href']
                entry_url = urljoin(BASE_URL, href)
                entry_response = session.get(entry_url)
                if entry_response.status_code != 200:
                    print(f'Failed to retrieve page for entry {entry_name}')
                    continue

                entry_soup = BeautifulSoup(entry_response.content, 'html.parser')
                definitions_divs = entry_soup.find_all('div', class_='definition')
                definitions = []
                for definition_div in definitions_divs:
                    definition_text = ''
                    example_text = ''
                    synonyms = set()  # Unique synonyms
                    votes = 0
                    # Extract text content from the 'p' tags
                    definition_p = definition_div.find_all('p')
                    for p in definition_p:
                        # Examples are in italics
                        examples = p.find('i')
                        # Synonyms are in buttons
                        synonym_btns = p.find_all(class_='btn btn-mini btn-warning')
                        # Upload description marked with 'small' tag
                        upload_desc = p.find('small')
                        if examples:
                            example_text = examples.text.strip()
                        elif synonym_btns:
                            synonyms.update(btn.text for btn in synonym_btns)
                        elif upload_desc:  # Parse number of votes
                            votes = int(re.search(r'votos\s+(-?\d+)', upload_desc.text).group(1))
                        # If none of the above, treat it as definition text
                        else:
                            definition_text += p.text.strip()
                    definition_data = {
                        'definition_text': definition_text,
                        'example_text': example_text,
                        'synonyms': list(synonyms),
                        'votes': votes
                    }
                    definitions.append(definition_data)
                all_entries[entry_name] = definitions
                pbar.update(1)
        print(f'Page for letter "{letter}" complete')
    return all_entries


if __name__ == '__main__':
    entries = scrape_diccionariochileno()
    # Print:
    buffer = '\n                     '
    for entry_name, definitions in entries.items():
        print(f'Entry: {entry_name}')
        for i, definition_data in enumerate(definitions, start=1):
            print(f'Definition {i}:')
            indented_definition = buffer.join(definition_data["definition_text"].split('\n'))
            print(f'  Definition Text: [{buffer}{indented_definition}{buffer[:-2]}]')
            indented_examples = buffer.join(definition_data["example_text"].split('\n'))
            print(f'  Example Text:    [{buffer}{indented_examples}{buffer[:-2]}]')
            print(f'  Synonyms:        {definition_data["synonyms"] or "None"}')
            print(f'  # of Votes: {definition_data["votes"]}')
            print()
