import ntpath
from glossaryList import WordList

glossary_list = WordList()

word_list = []
filePath = 'data/Black-Disability/CSV/Work in the INtersection- A Black Feminist Disability Framework by Moya Bailey and Izetta Autumn Mobley.csv'
fileName = ntpath.basename(filePath)[0:-4]
words_fileName = fileName.split()
for word in words_fileName:
    if word.capitalize() in glossary_list:
        word_list.append(word)
    else:
        pass

for value in word_list:
    print(value)