import configparser
from hashlib import new
from mimetypes import init
from operator import delitem
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
from util.util import WikibaseImporter
from logger import DebugLogger
import csv
import ntpath as nt

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()

wikibase = pywikibot.Site("wikidata", "wikidata")


class CreateTriples:
    def __init__(self, wikibase, wikidata, sparql):
        self.sparql = sparql
        self.wikibase = wikibase
        self.wikidata_repo = wikibase.data_repository()
        self.wikibase_importer = WikibaseImporter(
            self.wikibase_repo, self.wikibase_repo)

    def searchWikiItem(self, label):
        if label is None:
            return True
        params = {'action': 'wbsearchentities', 'format': 'json', 'language': 'en',
                  'type': 'item', 'limit': 1, 'search': label}

        request = self.wikibase._simple_request(**params)
        result = request.submit()
        print(result)
        return True if len(result['search']) > 0 else False

    def getWikiItemSparql(self, label):
        query = ""
        if (self.wikidata_code_property_id is not None):
            query = """
                select ?label ?s where {
                    ?s ?p ?o
                    ?s rdfs:label ?label
                    FILTER NOT EXISTS{?s wdt:""" + self.wikidata_code_property_id + """ []}
                    FILTER(lang(?label) = 'fr' || lang(?label) = 'en)
                }
            """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)  
        results = self.sparql.query().convert()
        print(results)

        if(len(results['results']['bindings']) > 0):
            return True
        else:
            return False

    wikidata_code_property_id = None

    def capitaliseFirstLetter(self, word):
        return word.capitalize()

    def getClaim(self, item_id):
        entity = pywikibot.ItemPage(self.wikidata_repo, item_id)
        claims = entity.get(u'claims')
        return claims

    def importWikiDataConcept(self, wd_qid, wb_qid):
        wikibase_item = pywikibot.ItemPage(self.wikibase_repo, wd_qid)
        wikibase_item.get()

    def create_claim(self, subject_string, property_string, object_string, claims_hash, qualifier_prop=None, qualifier_target=None):
        new_item = {}
        newClaims = []
        data = {}
        subject_result = self.getWikiItemSparql(
            self.capitaliseFirstLetter(subject_string).rstrip())
        subject_item = {}
        subject_id = None
        if (len(subject_result['results']['bindings']) > 0):
            subject_uri = subject_result['results']['bindings'][0]['s']['value']
            subject_id = subject_uri.split("/")[-1]
            subject_item = pywikibot.ItemPage(self.wikibase_repo, subject_id)
            subject_item.get()
            print(subject_item.id)

        else:
            



    def reading_xlsx_and_process(self, file_url):
        claims_hash = {}
        self.getWikiDataItemtifier()

        with open(file_url) as csv_file:
            file_name = nt.basename(csv_file)
            subject = file_name.rstrip(".pdf .csv")
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (line_count == 0):
                    line_count = line_count + 1
                    continue

                if (row[1] == None or row[2] == None or row[3] == None):
                    line_count = line_count + 1
                    continue

                else:
                    try:
                        print(f"currently inserting claim. Subject : ")
                    except Exception as e:
