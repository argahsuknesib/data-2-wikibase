from cProfile import label
from unittest import result
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

def main():

    label = "Career"

    query = """
        select ?label ?s where 
        {
            ?s ?p ?o.
            ?s rdfs:label ?label.
            FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
            FILTER(?label = ' """ + label + """ ')
        }
    
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)


if __name__ == '__main__':
    main()