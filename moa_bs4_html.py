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
    pattern = r'^[A-Z]\d{3}$'

    # Use re.match to check if the string matches the pattern
    return bool(re.match(pattern, s))

def split_camel_case(s):
    # Use a regular expression to find transitions between lowercase to uppercase or digits
    return re.findall(r'[A-Z][a-z]*|[0-9]+', s)

def process_file(file_path, csv_writer):

    running_category = ''
    tenant = ''
    running = 0
    data_out = []

    data_out.append("running_row")
    data_out.append("date_captured")
    data_out.append("location_category")
    data_out.append("store")
    data_out.append("address")
    csv_writer.writerow(data_out)
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

                    if row.find("strong"):
                        running_category = clean_text(row.find("strong").get_text())

                    if row.select("tr > td > table > tbody > tr > td > a"):

                        tenants = row.select("tr > td > table > tbody > tr > td > a")
                        for tenant in tenants:
                            running += 1

                            # Store information is just a bear

                            store_url_raw = tenant['href']
                            store_url_address_arr = store_url_raw.split('_')[5:]
                            tenant_value = clean_text(tenant.get_text())
                            tv_arr = tenant_value.split()

                            # Addressing is a complete mix
                            # If there's a valid address at the end of the
                            # tv_arr, then grab it and get on with your life
                            # Otherwise go through the gymanastics
                            # - Test for `tenant` for anchors
                            # - Test for `park` for park based
                            # [ ] TODO - Fix

                            test_addr = tv_arr[-1]

                            if is_regular_adddress(test_addr):
                                store = ' '.join(tv_arr[0:-1])
                                address = test_addr
                            else:
                                address = store_url_address_arr[-1].split('.')[0]
                                if not is_regular_adddress(address):
                                    address_arr = split_camel_case(address)
                                    address = ' '.join(address_arr)

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

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        process_file("./pages/" + filename, csv_writer)

    # csv_writer.flush()
    csvfile.flush()
    csvfile.close()
    # process_file(path)
