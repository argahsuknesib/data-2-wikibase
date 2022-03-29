import csv

def WordList():
    filePath = 'data/glossary/DRPI-glossary.csv'
    glossary_words = []
    with open(filePath, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for line in csv_reader:
            for value in line:
                if line_count > 1:
                    if value != '':
                        glossary_words.append(value.capitalize())
            line_count = line_count + 1
    return glossary_words

