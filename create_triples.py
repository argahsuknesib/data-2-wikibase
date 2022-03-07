from logging import exception
from venv import create
import pywikibot
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from util.util import WikibaseImporter
import configparser
import ntpath as nt
import csv

config = configparser.ConfigParser()
config.read('config/application.config.ini')
wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()
wikidata = pywikibot.Site("wikidata", "wikidata")
fileXLSX = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .xlsx"
fileCSV = "data/BIPOC/(1977) The Combahee River Collective Statement.pdf .csv"

class CreateTriples:
    def __init__(self, wikibase, wikidata, sparql):
        self.sparql = sparql
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.wikibase_importer = WikibaseImporter(self.wikibase_repo, self.wikidata_repo)


    def createItem(self, label, description, key, entity_list):
        if (self.capitaliseFirstLetter(key.rstrip()) in entity_list):
            return entity_list
        entity = self.getWikiItemSparql(
            self.capitaliseFirstLetter(key.rstrip())
        )
        isExistAPI = self.getWikiItemSparql()


    def process_files(self, file_url):
        with open(fileCSV) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter= ',')
            line_count = 0

            for row in csv_reader:
                if (line_count == 0):
                    line_count = line_count + 1
                if(row[1] == None or row[2] == None or row[3] == None):
                    line_count = line_count + 1
                    continue
                else:
                    try:
                        subject = nt.basename(csv_file)


                    except Exception as exception:
                        print(exception)

def main():
    createTriples = CreateTriples(wikibase, wikidata, sparql)
    file_nonCSV = pd.read_excel(fileXLSX)
    file_nonCSV.to_csv(fileCSV)
    createTriples.process_files(fileCSV)


if __name__ == "__main__":
    main()