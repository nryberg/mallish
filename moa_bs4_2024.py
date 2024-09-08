from re import X
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import re

output_csv = "./2024_listings_moa.csv"

# Remove extra unprintable characters and spaces
def clean_text(dirty_text):
    working = dirty_text.replace("\t", "")
    working = working.replace("\n", "")
    working = working.replace("\r", "")
    working = ' '.join(working.split())

    return working

def is_regular_adddress(s):
    # Regular expression to match an uppercase letter followed by exactly three digits
    pattern = r'^[A-Za-z]\d{3}$'

    # Use re.match to check if the string matches the pattern
    return bool(re.match(pattern, s))

def is_parens_address(s):
    pattern = r'^\(.*\)$'
    return bool(re.match(pattern, s))


def split_camel_case(s):
    # Use a regular expression to find transitions between lowercase to uppercase or digits
    return re.findall(r'[A-Z][a-z]*|[0-9]+', s)

def old_school_address(new_school_address):

    chunks = new_school_address.split()

    if len(chunks) > 1:

        direction = chunks[1]

        og = direction[0] + chunks[0]

        return og
    else:
        return new_school_address


def process_file(file_path, csv_writer):

    running_category = ''
    tenant = ''
    running = 0
    data_out = []
    category = ''


    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    formatted_date = '2024-09-02'  # TODO - automate this

    divs = soup.find_all('div', class_="card__tile card__tile--single bg--white") # div class="card__tile card__tile--single bg--white

    for card in divs:
        running += 1

        store = card.find('h3', class_="heading--card-title dsDirectory").getText()
        store = clean_text(store)
        category_elem = card.find('div', attrs={'role': 'heading'})

        if category_elem != None:
            category_slash = category_elem.getText()
            category = category_slash.split('/')[0]

        else:
            category = 'n/a'

        address_elem = card.find('div', class_="heading--card-info-location").span
        address = address_elem.getText()

        address = old_school_address(address)

        category = clean_text(category)

        print(running, " : ", category, " | ", store, '-', address)

        csv_writer.writerow([running, formatted_date, category, store, address])


if __name__ == '__main__':
    path = "pages/2024/A_Directory _ Mall of America® copy.htm"

    csvfile = open(output_csv, 'w')
    csv_writer = csv.writer(csvfile)


    csv_writer.writerow(["Row Number", "Date Captured", "Location Category", "Store", "Address"])

    process_file(path, csv_writer)

    # csv_writer.flush()
    csvfile.flush()
    csvfile.close()
    # process_file(path)
