import csv
import sys
import configparser
import traceback
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()

wikidata = pywikibot.Site("wikidata", "wikidata")


class UploadItem():
    def __init__(self, wikibase):
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
        self.class_entities = {}
        self.properties = {}

    def capitaliseFirstLetter(self, word):
        return word.capitalize()

    def read_language_list(self):
        filepath = 'util/language_list'
        lang_list = []
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                lang_list.append(line.replace("\n", ""))
                line = fp.readline()
        return lang_list

    def createItem(self, label, description, key, entity_list):
        pass

    def readCSV(self, filePath):
        entity_list = {}
        with open(filePath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for line in csv_reader:
                new_item = {}
                print(f'processing the glossary line {line_count}')
                try:
                    glossary_class = pywikibot.ItemPage(self.wikibase_repo)
                    glossary_class.editLabels(labels={'en': line['Label'].capitalize(
                    )}, summary='adding the main label to add the synonyms later')
                    glossary_class.editDescriptions(
                        descriptions={'en': 'This entity is a word from the glossary'})
                    
                    """
                    for one alias
                    """
                    #glossary_class.editAlias(aliases={'en' : [line['alias1'].capitalize()]}, summary='adding the synonyms to the label')
                    """
                    for two alias
                    """
                    #glossary_class.editAlias(aliases={'en' : [line['alias1'].capitalize(), line['alias2'].capitalize()]}, summary='adding the synonyms to the label')
                    """
                    for three alias
                    """    
                    #glossary_class.editAlias(aliases={'en' : [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize()]}, summary = 'adding the synonyms to the label')
                    """
                    for four alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for five alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for six alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for seven alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for eight alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for nine alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for ten alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for eleven alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for twelve alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize(), line['alias12'].capitalize() ]}, summary = 'adding the synonymns to the label')
                    """
                    for thirteen alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize(), line['alias12'].capitalize(), line['alias13'].capitalize() ]}, summary = 'adding the synonymns to the label')
                    """
                    for fourteen alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize(), line['alias12'].capitalize(), line['alias13'].capitalize(), line['alias14'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for fifteen alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize(), line['alias12'].capitalize(), line['alias13'].capitalize(), line['alias14'].capitalize(), line['alias15'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for sixteen alias
                    """
                    #glossary_class.editAlias(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(), line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize(), line['alias6'].capitalize(), line['alias7'].capitalize(), line['alias8'].capitalize(), line['alias9'].capitalize(), line['alias10'].capitalize(), line['alias11'].capitalize(), line['alias12'].capitalize(), line['alias13'].capitalize(), line['alias14'].capitalize(), line['alias15'].capitalize(), line['alias16'].capitalize()]}, summary = 'adding the synonymns to the label')
                    """
                    for twentyfour aliases
                    """

                    """
                    for seventytwo alias
                    """

                    # for i in range(1,80):
                    #     if line['alias%d'%i] == '':
                    #         pass
                    #     else:
                    #         glossary_class.editAliases(aliases={'en': [line['alias1'].capitalize(), line['alias2'].capitalize(),line['alias3'].capitalize(), line['alias4'].capitalize(), line['alias5'].capitalize()]}, summary='adding the synonyms to the label')
                    #     # if line['alias%d' % i] != '':
                    #     #     glossary_class.editAliases(aliases={'en': [line['alias%d' % i].capitalize()]}, summary='adding the synonyms to the label')
                    #     # else:
                    #     #     pass

                except Exception as e:
                    print('The exception encountered is, ', e)
                line_count = line_count + 1


def main():
    uploading_item = UploadItem(wikibase)
    # uploading_item.readCSV('data/glossary/DRPI-glossary-test.csv')
    uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-Label.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-OneAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-TwoAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-ThreeAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-FourAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-FiveAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-SixAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-SevenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-EightAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-NineAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-TenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-ElevenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-TwelveAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-ThirteenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-FourteenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-FifteenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-SixTeenAlias.csv')
    #uploading_item.readCSV('data/glossary/DRPI-Final/DRPI-ElevenAlias.csv')


if __name__ == '__main__':
    main()
