import csv
import sys
import configparser
import traceback
import pywikibot
from logger import DebugLogger
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
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0 
            for row in csv_reader:
                new_item = {}
                print(f'processing the glossary line {line_count}')
                if (line_count == 0):
                    line_count = line_count + 1
                    continue
                else:
                    try:
                        glossary_class = pywikibot.ItemPage(self.wikibase_repo)
                        



                    except Exception as e:
                        error_message = f"Error encountered while creating item: {row[0].rstrip()} Row count: {line_count}"
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        tb = traceback.extract_tb(exc_tb)[-1]
                        err_trace = f"error trace : >>> + {exc_type}, method: {tb[2]}, line-no: {tb[1]}"
                        logger = DebugLogger()
                        logger.logError('Create Item', e, exc_type, exc_obj, exc_tb, tb, error_message)
                    line_count = line_count + 1

def main():
    uploading_item = UploadItem(wikibase)
    uploading_item.get_class_entity()
    uploading_item.readCSV('data/glossary/DRPI-glossary.csv')

if __name__ == '__main__' :
    main()