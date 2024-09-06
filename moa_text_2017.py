from re import X
import os
import csv
import re

output_csv = "./2017_listings_moa_text.csv"
input_path = "./data/2017_listings.txt"

# Remove extra unprintable characters and spaces
def clean_text(dirty_text):
    working = dirty_text.replace("\t", "")
    working = working.replace("\n", "")
    working = working.replace("\r", "")
    working = ' '.join(working.split())

    return working

def is_moa_store_adddress(s):
    # Regular expression to match an uppercase letter followed by exactly three digits
    pattern = r'^[A-Za-z]\d{3}$'

    # Use re.match to check if the string matches the pattern
    return bool(re.match(pattern, s))


def is_phone_number(s):
    # Regular expression to match various phone number formats
    # Basic 10-digit number: 1234567890
    # Number with hyphens: 123-456-7890
    # Number with parentheses and space: (123) 456-7890
    # Number with international code: +1 123-456-7890
    pattern = r'^(\+?\d{1,2}\s?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}$'

    # Use re.match to check if the entire string matches the phone number pattern
    return bool(re.match(pattern, s))

def has_spaced_letters(s):
    # Regular expression to check if the string contains letters separated by spaces
    pattern = r'([A-Z]\s){2}[A-Z]'

    # Use re.match to check if the string matches the pattern
    return bool(re.match(pattern, s))

def remove_trailing_m_w_c(s):
    # Regular expression to match 'm', 'w', or 'c' followed by optional spaces at the end of the string
    pattern = r'(m\s?w\s?c?|m\s?w?|w\s?c?|m|w|c)\s*$'

    # Use re.sub to remove the matched characters
    return re.sub(pattern, '', s).strip()

if __name__ == '__main__':
    csvfile = open(output_csv, 'w')
    csv_writer = csv.writer(csvfile)
    row_num = 0
    date = '2017-10-01'
    # csv_writer.writerow
    data = ['row', 'date', 'category', 'store', 'address', 'phone']
    csv_writer.writerow(data)
    f = open(input_path)
    data = []
    category = ''
    phone = ''
    address = ''
    for line in f:
        row_num += 1
        line = clean_text(line)

        if has_spaced_letters(line):
            category = ''.join(line.split())
        else:
            val_arr = line.split()

            # for element in reversed(val_arr):
            for i in range(len(val_arr) - 1, -1, -1):
                element = val_arr[i]

                if is_phone_number(element):
                    phone = element

                if is_moa_store_adddress(element):
                    address = element

                    store = ' '.join(val_arr[:i])

                    if category == 'APPAREL':
                        store = remove_trailing_m_w_c(store)

                    csv_writer.writerow([row_num, date, category, store, address, phone])
            # print(row_num, " : ", store, " | ", address, " | ",  phone)

        phone = ''
        address = ''
        store = ''
    csvfile.flush()
    csvfile.close()

    f.close()
    # process_file(path)
