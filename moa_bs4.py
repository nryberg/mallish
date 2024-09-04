from re import X
from bs4 import BeautifulSoup
import os
import csv

output_csv = "./listings_moa.csv"

# Remove extra unprintable characters and spaces
def clean_text(dirty_text):
    working = dirty_text.replace("\t", "")
    working = working.replace("\n", "")
    working = working.replace("\r", "")
    working = ' '.join(working.split())

    return working

def process_file(file_path, csv_writer):

    running_category = ''
    tenant = ''
    running = 0
    data_out = []

    data_out.append("date_captured")
    data_out.append("running_row")
    data_out.append("location_category")
    data_out.append("tenant")
    csv_writer.writerow(data_out)
    data_out = []

    with open(file_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    capture_date = soup.find('td', id="displayMonthEl")
    mall_date = ' '.join(capture_date.get("title").split('here:')[1:]).strip()
    # print(capture_date.get("title").split(':')[1:])
    print(mall_date)

    listingContents = soup.findAll("div", id="listingContent")

    for listingContent in listingContents:
        # print(listingContent.prettify())
        if listingContent and listingContent.find("table"):
            sections = listingContent.select("div > table > tbody")

            for section in sections:
            # print(listings.prettify())
                for row in section.find_all("tr", recursive=False):
                    #category_node = row.find("strong")

                    if row.find("strong"):
                        running_category = clean_text(row.find("strong").get_text())

                    if row.select("tr > td > table > tbody > tr > td > a"):

                        tenants = row.select("tr > td > table > tbody > tr > td > a")
                        for tenant in tenants:
                            running += 1
                            tenant_value = clean_text(tenant.get_text())
                            data_out.append(mall_date)
                            data_out.append(running)
                            data_out.append(running_category)
                            data_out.append(tenant_value)
                            csv_writer.writerow(data_out)
                            data_out = []
                            # print(mall_date, "-", running, ":",  running_category, "- " , tenant_value) # tenant.get_text())
                    # if running >= 10 :
                    #     break
    # print(listings.prettify())


if __name__ == '__main__':
    path = "pages/2006_06_02_Mall of America - Mall Directory.htm"

    directory = os.fsencode("./pages")

    csvfile = open(output_csv, 'w')
    csv_writer = csv.writer(csvfile)
    # csv_writer.writerow

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        print(filename)
        process_file("./pages/" + filename, csv_writer)

    # csv_writer.flush()
    csvfile.flush()
    csvfile.close()
    # process_file(path)
