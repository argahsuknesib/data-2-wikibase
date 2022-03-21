import csv

with open('data/Black-Disability/CSV/Black Disability Gone Viral word.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',')
    line_count = 0
    for line in csv_reader:
        print(f'currently on the line {line_count}')
        try:
            paragraph_text = line['Paragraph'].strip()
            print(paragraph_text)
        except Exception as e:
            print(e)

        line_count = line_count + 1