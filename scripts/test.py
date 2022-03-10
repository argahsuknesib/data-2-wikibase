import csv

with open('data/glossary/DRPI-glossary.csv', 'r', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for line in csv_reader:
        # print('currently processing the line number : ', line_count)
        try:
            # print("Label : ", line['Label'])
            # print("Alias1 : ", line['alias1'])
            # print("Alias2 :", line['alias2'])
            # print("Alias3 : ", line['alias3'])
            # for i in range(1, 3):
            #     print(line['alias%d'%i].capitalize())
            # if line['alias1'] != '':
            #     print(line['alias1'])
            if(line['alias1']) == '':
                print(line_count, 'yes')
        except Exception as e:
            pass
        line_count = line_count + 1
