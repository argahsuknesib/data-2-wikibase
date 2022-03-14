import pandas as pd
import ntpath


fileToRead = "data/Black-Disability/Working definition of ableism word.pdf .xlsx"
fileName = ntpath.basename(fileToRead)[0:-10]
print(fileName)


read_file = pd.read_excel(fileToRead)
read_file.to_csv("data/Black-Disability/CSV/" + fileTitle+ ".csv", index=None, header=True)