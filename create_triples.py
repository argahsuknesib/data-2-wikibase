import csv
import configparser
from unittest import result
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
from util.util import WikibaseImporter

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()

wikidata = pywikibot.Site("wikidata", "wikidata")


class CreateTriples:
    def __init__(self, wikibase, wikidata, sparql):
        self.sparql = sparql
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.wikidata_repo = wikibase.data_repository()
        self.wikibase_importer = WikibaseImporter(
            self.wikibase_repo, self.wikidata_repo
        )

    def searchWikiItem(self, label):
        if label is None:
            return True
        params = {'action': 'wbsearchentities', 'format': 'json',
                  'language': 'en', 'type': 'item', 'limit': 1}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        print(result)
        return True if len(result['search'] > 0) else False

    def searchWikiItemSparql(self, label):
        query = """
            select ?label ?s where {
                ?s ?p ?o.
                ?s rdfs:label ?label.
                FILTER(lang(?label)='fr') || label(?label) = 'en')
                FILTER(?label = '""" + label + """'@en)
            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        print(results)
        if (len(results['results']['bindings']) > 0):
            return True
        else:
            return False

    wikidata_code_property_id = None

    def getWikiDataItentifier(self):
        query = """
        
            select ?wikicode
            {
                ?wikicode rdfs:label ?plabel
                FILTER(?plabel = 'Wikidata QID'@en)
                FILTER(lang(?plabel) = 'fr' || lang(?plabel) = 'en')
            }
            limit 1
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        if(len(results['results']['bindings']) > 0):
            self.wikidata_code_property_id = results['results']['bindings'][0]['wikicode']['value'].split(
                "/"
            )[-1]

        return results

    def getItemIdByWikidataQID(self, qid):
        query = """"
        
            select ?s ?label
            where {
                ?s ?p ?o;
                rdfs:label ?label;
                wdt:""" + self.wikidata_code_property_id + """  ' """ + qid + """ '.
            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        if (len(results['results']['bindings']) > 0):
            return results['results']['bindings'][0]['s']['value'].split("/")[-1]
        else:
            return None

    def getWikiItemSparql(self, label):
        query = ""
        if (self.wikidata_code_property_id is not None):
            query = """ 
                select ?label ?s where 
                {
                    ?s ?p ?o.
                    ?s rdfs:label ?label
                    FILTER NOT EXISTS {?s wdt:""" + self.wikidata_code_property_id + """ []}
                    FILTER (lang(?label)='fr' || lang(?label) = 'en')
                    FILTER(?label = '""" + label + """ '@en)
                }
            """

        else:
            query = """ 
                select ?label ?s where {
                    ?s ?p ?o.
                    ?s rdfs:label ?label .
                    FILTER(lang(?label) = 'fr') || lang(?label)= 'en')
                    FILTER(?label = '""" + label + """'@en)
                }
            """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)