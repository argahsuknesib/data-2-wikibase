import csv

filePath = "data/Black-Disability/CSV/(1977) The Combahee River Collective Statement.csv"

with open(filePath, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter = ',')
    line_count = 0
    for line in csv_reader:
        print(f'currently on the line {line_count}')
        try:
            paragraph_text = line['Paragraph']
            paragraph_labels = []

            print(type(line['Paragraph']))

            for i in range(1, 15):
                if(line[f'Label {i}']) != "":
                    paragraph_labels.append(line[f'Label {i}'].capitalize())
            # print(paragraph_labels)


        except Exception as e:
            print('The exception encountered is ', e)
        line_count = line_count + 1