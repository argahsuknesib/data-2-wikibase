import csv
import configparser
from re import U
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
        results = self.sparql.query().convert()
        return results

    def getItems(self):
        pid = "P31"
        params = {'action': 'wbgetentities', 'ids': pid}
        request = self.wikibase._simple_request(**params)
        results = request.query()
        print(result["entities"][pid]["descriptions"])

    def capitalseFirstLetter(self, word):
        return word.capitalize()

    def getClaim(self, item_id):
        entity = pywikibot.ItemPage(self.wikibase_repo. item_id)
        claims = entity.get(u'claims')
        return claims

    def importWikiDataConcept(self, wd_qid, wb_qid):
        wikidata_item = pywikibot.ItemPage(self.wikidata_repo, wd_qid)
        wikidata_item.get()
        wikibase_item = pywikibot.ItemPage(self.wikibase_repo, wb_qid)
        wikibase_item.get()
        self.wikibase_importer.change_item_V2(
            wikidata_item, True, wikibase_item
        )

        return wikibase_item

    def linkWikidataItem(self, subject, qid):
        data = {}
        newClaims = []
        wikidata_item = None
        existing_item_id = self.getItemIdByWikidataQID(qid)
        if(existing_item_id is not None):
            wikidata_item = pywikibot.ItemPage(
                self.wikibase_repo, existing_item_id
            )
            wikidata_item.get()

        else:
            wikidata_item = self.importWikiDataConcept(qid, subject.id)
        property_result = self.getWikiItemSparql(
            'Has wikidata substitute item'
        )
        property_id = property_result['results']['bindings'][0]['s']['value'].split(
            "/"
        )[-1]

        property = pywikibot.PropertyPage(self.wikibase_repo, property_id)

        existing_claims = self.getClaim(subject.id)
        if u'' + property_id + '' in existing_claims[u'claims']:
            pywikibot.output(u'Error: Already item has link to wikidata substitute item')
            return subject
        claim == pywikibot.Claim(self.wikibase_repo, property_id, datatype=property.type)
        claim.setTarget(wikidata_item)
        newClaims.append(claim.toJSON())
        data['claims'] = newClaims
        subject.editEntity(data)
        return subject

    def create_claim(self, subject_string, property_string, object_string, claims_hash, qualifier_prop=None, qualifier_target=None):
        new_item = {}
        newClaims = []
        data = {}

        subject_result = self.getWikiItemSparql(
            self.capitalseFirstLetter(subject_string).rstrip()
        )
        subject_item = {}
        subject_id = None

        if (len(subject_result['results']['bindings']) > 0):
            subject_uri = subject_result['results']['bindings'][0]['s']['value']
            subject_id = subject_uri.split("/")[-1]
            subject_item = pywikibot.ItemPage(self.wikibase_repo, subject_id)
            subject_item.get()
            print(subject_item.id)

        else:
            pass
            


        

