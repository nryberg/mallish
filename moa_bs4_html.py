from re import X
from bs4 import BeautifulSoup
import os
import csv
from datetime import datetime
import re

output_csv = "./listings_moa.csv"

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

def process_file(file_path, csv_writer):

    running_category = ''
    tenant = ''
    running = 0
    data_out = []


    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    capture_date = soup.find('td', id="displayMonthEl")
    mall_date = ' '.join(capture_date.get("title").split('here:')[1:]).strip()
    date_obj = datetime.strptime(mall_date, '%H:%M:%S %b %d, %Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    print(formatted_date)

    listingContents = soup.findAll("div", id="listingContent")

    for listingContent in listingContents:
        if listingContent and listingContent.find("table"):
            sections = listingContent.select("div > table > tbody")

            for section in sections:
                for row in section.find_all("tr", recursive=False):



                    #category_node = row.find("strong")
                    # Is this a section header?
                    if row.find("strong"):
                        running_category = clean_text(row.find("strong").get_text())

                    # Is this a store listing section?
                    if row.select("tr > td > table > tbody > tr > td > a"):

                        tenant_links = row.select("tr > td > table > tbody > tr > td > a")
                        for tenant in tenant_links:
                            store = ''
                            address = ''

                            running += 1

                            store_url_raw = tenant['href']
                            store_url_arr = store_url_raw.split('_')[5:]

                            store_text_raw = clean_text(tenant.get_text())
                            store_text_arr = store_text_raw.split()

                            # Addressing is a complete mix
                            # If there's a valid address at the end of the
                            # tv_arr, then grab it and get on with your life
                            # Otherwise go through the gymanastics
                            # - Test for `tenant` for anchors
                            # - Test for `park` for park based
                            # [ ] TODO - Fix

                            store_text_test_addr = store_text_arr[-1]

                            # Fix parenthetical addresses

                            store_url_test = store_url_arr[-1].split('.')[0]

                            if store_text_raw.__contains__('Julius'):
                                print("Raw Text: ", store_text_raw)
                                print("Text Address Test: ", store_text_test_addr)
                                print("Text Array:", store_text_arr)
                                print("Raw URL:", store_url_raw)
                                print("URL_Test:", store_url_test)
                                print("URL Arr:", store_url_arr)



                            if store_url_test == 'tenant':  # Department Stores
                                store = store_text_raw
                                address = 'Anchor'
                            elif store_url_test == 'park':  # Theme Park Stores
                                store = store_text_raw
                                address = 'Theme Park'
                            elif store_url_test == 'Underwater':
                                store = store_text_raw
                                address = 'Underwater World'
                            elif is_regular_adddress(store_text_test_addr):
                                store = ' '.join(store_text_arr[0:-1])
                                address = store_text_test_addr
                            elif is_parens_address(store_text_test_addr):
                                store = ' '.join(store_text_arr[0:-1])
                                address = re.sub(r'^\(|\)$', '', store_text_test_addr)
                            else:
                                if is_regular_adddress(store_url_test):
                                    store = store_text_raw
                                    address = store_url_test
                                else:

                                    address_arr = split_camel_case(store_url_test)
                                    address = ' '.join(address_arr)
                                    store = store_text_raw

                            if running_category == 'Specialty Retail - Carts' and address == '':
                                address = 'Cart'

                            # Build the array for output
                            data_out = []
                            data_out.append(running)
                            data_out.append(formatted_date)
                            data_out.append(running_category)
                            data_out.append(store)
                            data_out.append(address)

                            csv_writer.writerow(data_out)
                            data_out = []
                    # if running >= 10 :
                    #     break
    # print(listings.prettify())


if __name__ == '__main__':
    path = "pages/2006_06_02_Mall of America - Mall Directory.htm"

    directory = os.fsencode("./pages")

    csvfile = open(output_csv, 'w')
    csv_writer = csv.writer(csvfile)


    csv_writer.writerow(["Row Number", "Date Captured", "Location Category", "Store", "Address"])

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        process_file("./pages/" + filename, csv_writer)

    # csv_writer.flush()
    csvfile.flush()
    csvfile.close()
    # process_file(path)
