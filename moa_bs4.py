from re import X
from bs4 import BeautifulSoup

running_category = ''
tenant = ''
running = 0

with open("./pages/2006_06_02_Mall of America - Mall Directory.htm") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

listingContents = soup.findAll("div", id="listingContent")

for listingContent in listingContents:
    # print(listingContent.prettify())
    if listingContent and listingContent.find("table"):
        listings = listingContent.find("table")
        print(listings.prettify())
        for row in listings.select("tr"):
            testnode = row.find("strong")

            if testnode != None:
                running_category = testnode.get_text()
            elif testnode == None:
                # print(row.prettify())
                tenants = row.select("tr > td > table > tbody > tr > td > a")
                for tenant in tenants:
                    running += 1
                    tenant_value = tenant.get_text()
                    print(running, running_category, tenant_value) # tenant.get_text())
                    if running >= 10 :
                        break
# print(listings.prettify())
