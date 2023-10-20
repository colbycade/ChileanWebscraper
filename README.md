![img.png](resources/chilean_flag.png)
# Chilean Dictionary Webscraper
### Background
I lived in Chile for a year and loved learning the language, especially the "chilenismos". 
I used this website when I didn't know what something meant. 
It's a crowdsourced collection of slang and their definitions similar to UrbanDictionary.
This project isn't neccesarily that useful, but I thought it would be fun exercise to practice Python, data cleaning, SQL, and version control.

## Description
This is a basic webscraper that collects crowdsourced Chilean slang words/phrases and definitions from the website diccionariochileno.cl and imports into a local MySQL database for analysis.

## Installation Instructions
Begin by cloning the repository to your GitHub.

You need to set up a MySQL server to store all the words (see `model.png` under the `resources` folder for schema). 
I ran one locally, but you should specify your hostname as well a username and password in the `update_db.py` file. 
Under `resources` there is a file called `DBsetup.sql` that you can use to set up the database and tables.

After the server is running, make sure to `pip install` the packages listed in the `requirements.txt` file under `resources`. 
These are used to communicate with the webpage and database, parse the html, and add progress bars to the terminal.

You should now be able to run the `main.py` script to populate the database. 
Uncomment the `print_def_data(entry_name, definition_data)` function on line 25 to see a printout of the entries. 
The website organizes entries by letter, so you can change the `ALPHABET` string to only certain letters if you don't want to go through every page in one go (it takes 2-3 minutes to go through all of them).

I also created an online Oracle database so I could learn how to use GitHub workflows to automatically update the database.
The workflow `weekly_update.yml` updates the database automatically every week. 
You can disable it by removing the `schedule:` lines, renaming the file to include special characters/spaces, or by simply deleting the file.

## Uses
Like I said, this isn't the most useful project, but it's fun to look through all the words.
You can also run queries on the database. I included some interesting/useful queries in the `Example_Quereies.sql` file under `resources`.

## Extra
While in Chile, I wrote down every word or phrase that I didn't recognize or thought was interesting/useful, organized them by frequency and other categories, then collected them all into a spreadsheet for study/reference.
It currently contains about 3,000 entries, and I have quite a few more that I haven't yet entered. 
That spreadsheet can be accessed here if interested: https://docs.google.com/spreadsheets/d/1n-BV4boWKd38noRMt-ku7NNEx_l5XblBNe03zxAd6cs/edit?usp=sharing
