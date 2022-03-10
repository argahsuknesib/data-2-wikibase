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
                    glossary_class.editLabels(labels={line['Label'].capitalize(
                    )}, summary='adding the main label to add the synonyms later')
                    glossary_class.editDescriptions()
                    for i in range(1, 79):
                        glossary_class.editAliases(aliases={'en': [line['alias%d' % i].capitalize(
                        )]}, summary='adding the synonyms to the label')

                except Exception as e:
                    print('The exception encountered is, ', e)
                line_count = line_count + 1


def main():
    uploading_item = UploadItem(wikibase)
    uploading_item.get_class_entity()
    uploading_item.readCSV('data/glossary/DRPI-glossary.csv')


if __name__ == '__main__':
    main()