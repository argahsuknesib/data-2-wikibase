import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
import configparser

config = configparser.ConfigParser()
config.read('config/application.config.ini')

sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()
wikidata = pywikibot.Site("wikidata", "wikidata")
wikibase = pywikibot.Site("my", "my")
wikibase_repo = wikibase.data_repository()


class QueryExecuter():
    def __init__(self, wikibase):
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
        self.pywikibot = pywikibot
    
    def SQE(self, label):
        query = """
        select distinct ?s ?label  where
        {
            ?s ?p ?o;
            skos:altLabel ?label.
            FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
            FILTER(?label = ' """ + label + """   ') 
       }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        item_qid = results['results']['bindings'][0]['s']['value'].split("/")[-1]
        if (item_qid):
            #item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
            print(item_qid)

def main():
    queryValue = QueryExecuter(wikibase)
    queryValue.SQE('')
if __name__ == '__main__':
    main()
