from re import X
from bs4 import BeautifulSoup
import os

# Remove extra unprintable characters and spaces
def clean_text(dirty_text):
    working = dirty_text.replace("\t", "")
    working = working.replace("\n", "")
    working = working.replace("\r", "")
    working = ' '.join(working.split())

    return working

running_category = ''
tenant = ''
running = 0

directory = os.fsencode("./pages")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(os.path.join(directory, filename))

with open("./pages/2006_06_02_Mall of America - Mall Directory.htm") as fp:
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
                        # print(running, ":",  running_category, "- " , tenant_value) # tenant.get_text())
                # if running >= 10 :
                #     break
# print(listings.prettify())
