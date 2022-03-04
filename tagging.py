import pandas as pd
import csv
import ntpath as nt

from xlsx2wikibase import main, readingExcel
fileToUpload = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .xlsx"
fileInCSV = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .csv"

def readingExcel():
    file_excel = pd.read_excel(fileToUpload)
    file_excel.to_csv(fileInCSV)

    with open(fileInCSV) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        for row in csv_reader:
            if (line_count == 0):
                line_count = line_count + 1
                continue
            if(row[1] == None or row[2] == None or row[3] == None):
                line_count = line_count + 1
                continue
            else:
                pass



def main():
    # readingExcel()
    readingFile()

if __name__ == "__main__":
    main()