import csv

with open('data/glossary/DRPI-glossary.csv', 'r', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        # print(line[0].capitalize())
        print(row)