import csv

with open('data/Black-Disability/CSV/Autistic while black How autism amplifies stereotypes by Catina Burkett.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',')
    line_count = 0
    for line in csv_reader:
        print(f'currently on the line {line_count}')
        try:
            print('paragraph_text_original')
            print(line['Paragraph'])
            paragraph_text = line['Paragraph'].strip()
            print('--------------------------')
            print('paragraph_text_stripped')
            print(line['Paragraph'])
            print(paragraph_text)
        except Exception as e:
            print(e)

        line_count = line_count + 1