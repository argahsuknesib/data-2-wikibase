import ntpath
from glossaryList import WordList

glossary_list = WordList()

word_list = []
filePath = 'data/Black-Disability/White Privilege & Inspiration Porn by Vilissa Thompson.csv'
fileName = ntpath.basename(filePath)[0:-4]
words_fileName = fileName.split()
for word in words_fileName:
    if word.capitalize() in glossary_list:
        word_list.append(word)
    else:
        pass

print(word_list)