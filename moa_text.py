from re import X
import os
import csv

output_csv = "./listings_moa_text.csv"
input_path = "./data/1994_listings.md"

# Remove extra unprintable characters and spaces
def clean_text(dirty_text):
    working = dirty_text.replace("\t", "")
    working = working.replace("\n", "")
    working = working.replace("\r", "")
    working = ' '.join(working.split())

    return working

if __name__ == '__main__':
    csvfile = open(output_csv, 'w')
    csv_writer = csv.writer(csvfile)

    date = '1994-01-01'
    # csv_writer.writerow
    data = ['row', 'date', 'category', 'store', 'address', 'phone']
    csv_writer.writerow(data)
    f = open(input_path)
    row = 0
    category = ''
    rocker = 1
    store = ''
    address = ''
    phone = ''
    data = []
    for line in f:

        rocker += 1
        line = clean_text(line)

        if line[0:2] == "##":
            category = line[3:]
            # print("HEADER", category)
            rocker = 0

        if rocker == 1:
            store = line
        elif rocker == 2:
            address = line
        elif rocker == 3:
            row += 1
            phone = line
            rocker = 0
            data = [row, date, category, store, address, phone]
            output = ','.join(map(str, data))
            # print(output)
            csv_writer.writerow(data)
            data = []

        # print(row, line)

    # csv_writer.flush()
    csvfile.flush()
    csvfile.close()

    f.close()
    # process_file(path)
