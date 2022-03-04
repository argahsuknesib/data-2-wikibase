import pandas as pd
import ntpath as nt
import csv
fileToUpload = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .xlsx"
fileInCSV = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .csv"


def readingExcel():
    file_excel = pd.read_excel(fileToUpload)
    file_excel.to_csv(fileInCSV)
    with open(fileInCSV) as csv_file:
        csv_file = csv.DictReader(csv_file, delimiter = ",")
        line_count = 0
        for row in csv_file:
            # print(f' the current line number is {line_count}')
            if line_count == 0:
                # print(f' column headings are {" ,".join(row)}')
                line_count = line_count + 1
            else :
                try:
                    # for value in range(2, 10):
                    #     print(row[value])
                    print(row['Paragraph'])
                    # print(f' column values are {",".join(row)}')
                    line_count = line_count + 1
                except Exception as e:
                    print('There has been an exception encountered, which is : ', e)

def readingFile():
    file_name = nt.basename(fileInCSV)
    print(file_name[:-4])


def main():
    readingExcel()


if __name__ == "__main__":
    main()
