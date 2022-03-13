import csv
import configparser
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()

wikidata = pywikibot.Site("wikidata", "wikidata")

class UploadLabel():
    def __init__(self, wikibase):
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
        self.class_entities = {}
        self.properties = {}

    def capitaliseFirstLetter(self, word):
        return word.capitalize()

    def get_class_entity(self):
        labels = ["Document", "Topic", "Wikidata", "Paragraph", "Disability rights wiki"]
        for label in labels:
            object_result = self.getWikiItemSparql(
                self.capitaliseFirstLetter(label).rstrip()
            )
            if (len(object_result['results']['bindings']) > 0):
                object_uri = object_result['results']['bindings'][0]['s']['value']
                object_id = object_uri.split("/")[-1]
                object_item = pywikibot.ItemPage(self.wikibase_repo, object_id)
                object_item.get()
                self.class_entities[label] = object_item
                print(object_id)

        prop_labels = ["instance of", "part of", "has subtopic"]
        for p_label in prop_labels:
            property_result = self.getWikiItemSparql(p_label.rstrip().lstrip().lower())
            property_item = {}
            property_id = None

            if(len(property_result['results']['bindings']) > 0):
                property_uri = property_result['results']['bindings'][0]['s']['value']
                property_id = property_uri.split("/")[-1]
                property_item = pywikibot.PropertyPage(
                    self.wikibase_repo, property_id
                )
                property_item.get()
                self.properties[p_label] = property_item

    def searchWikiItem(self, label):
        if label is None:
            return True
        params = {'action':'wbsearchentities', 'format':'json', 'language':'en', 'type':'item', 'search':label}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        print(result)
        if (len(result['search']) > 0):
            for item in result['search']:
                if (item.get('label') == label):
                    return True
        return False

    def getWikiItemSparql(self, label):
        query = """
            select ?label ?s where
            {
                ?s ?p ?o.
                ?s rdfs:label ?label .
                FILTER(lang(?label)='fr') || lang(?label)='en')
                FILTER(?label = '""" + label + """'@en)
            }
        """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        return results

    def createItem(self, label, description, key, entity_list):
        if (self.capitaliseFirstLetter(key.rstrip()) in entity_list):
            return entity_list
        entity = self.getWikiItemSparql(self.capitaliseFirstLetter(key.rstrip()))
        isExistAPI = self.searchWikiItem(self.capitaliseFirstLetter(key.rstrip()))
        if (len(entity['results']['bindings'] == 0 and not isExistAPI)):
            data = {}
            print(f"inserting concept {key.rstrip()}")
            data['labels'] = label
            data['descriptions'] = description
            new_item = pywikibot.ItemPage(self.wikibase_repo)
            new_item.editEntity(data)
            



    def readCSVasDictionary(self, filePath):
        with open(filePath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ',')

