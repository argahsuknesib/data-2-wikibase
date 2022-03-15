import csv
import configparser
import ntpath
from pydoc import doc
from urllib import request
from xml.dom.minidom import Document
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
from configWikibaseID import ProductionConfig

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()
wikibase_repo = wikibase.data_repository()
class_entities = {}
properties = {}

wikidata = pywikibot.Site("wikidata", "wikidata")

def capitaliseFirstLetter(word):
    return word.capitalize()

def searchItem(label):
    if label is None:
        return False
    params = {'action': 'wbsearchentities', 'format': 'json',
                'language': 'en', 'type': 'item', 'limit': 100, 'search': label}
    request = wikibase._simple_request(**params)
    result = request.submit()
    return result


def searchExactWikiItem(label):
    if label is None:
        return True
    params = {'action': 'wbsearchentities', 'format': 'json',
                'language': 'en', 'type': 'item', 'limit': 1, 'search': label}
    request = wikibase._simple_request(**params)
    result = request.submit()
    print(result)
    if (len(result['search']) > 0):
        for item in result['search']:
            if (item.get('label') == label):
                return True
    return False

def searchWikiItem(label):
    query = """
        select ?label ?s where 
        {
            ?s ?p ?o.
            ?s rdfs:label ?label.
            FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
            FILTER(?label = '  """ + label + """ ')
        }
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if (len(results['results']['bindings']) > 0):
        return True
    else:
        return False

def getItemByAlias(label):
    query = """
    
        SELECT DISTINCT ?label ?s where 
        {
            ?s ?p ?o;
            skos:altLabel ?label.
            FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
            FILTER(?label = '  """ + label + """ ')
        }
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if (results.get('results', None) is not None and results.get('results').get('bindings') is not None
            and type(results.get('results').get('bindings')) is list and len(results.get('results').get('bindings')) > 0
            and results.get('results').get('bindings')[0] is not None and
            results.get('results').get('bindings')[
            0].get('s', None) is not None
            and results.get('results').get('bindings')[0].get('s').get('value', None) is not None
            ):

        item_qid = results['results']['bindings'][0]['s']['value'].split(
            "/")[-1]
        if (item_qid):
            item = pywikibot.ItemPage(wikibase_repo, item_qid)
            return item
        else:
            return False
    else:
        return False




def createDocumentEntity(label, description, key):
        search_result = searchWikiItem(capitaliseFirstLetter(key.rstrip()))
        is_exist = searchExactWikiItem(capitaliseFirstLetter(key.rstrip()))

        if (not search_result and not is_exist):
            data = {}
            print(f'inserting document entity {key.rstrip()}')
            data['labels'] = label
            data['descriptions'] = description
            new_item = pywikibot.ItemPage(wikibase_repo)
            new_item.editEntity(data, summary='Creating new item')

            new_claims = []
            claim_data = {}

            instance_claim = {}
            document_class_entity = pywikibot.ItemPage(
                wikibase_repo, f'{ProductionConfig.DOCUMENT_CLASS_QID}')
            document_class_entity.get()
            instance_of_property = pywikibot.PropertyPage(
                wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
            instance_of_property.get()
            instance_claim = pywikibot.Claim(
                wikibase_repo, instance_of_property.id, datatype=instance_of_property.Type)
            instance_claim.setTarget(document_class_entity)


            """
            uncomment this code about document URI just in case you 
            found a reason to add the actual link of the document.
            """

            # document_uri_property = self.pywikibot.PropertyPage(
            #     self.wikibase_repo, ProductionConfig.DOCUMENT_REFERENCE_URI_PROPERTY_PID)
            # document_uri_property.get()
            # document_uri_claim = self.pywikibot.Claim(
            #     self.wikibase_repo, document_uri_property.id, datatype=document_uri_property.Type)
            # document_uri_claim.setTarget(document_link)
            # new_claims.append(document_uri_claim.toJSON())

            new_claims.append(instance_claim.toJSON())
            claim_data['claims'] = new_claims
            new_item.editEntity(claim_data, summary='Adding new claims')

            return new_item
        else:
            entity = searchWikiItem(capitaliseFirstLetter(key.rstrip()))
            return entity

def create_sub_topic(topic, paragraph_entity, document_entity, lang):
    topic_entity = {}
    search_result = searchWikiItem(capitaliseFirstLetter(topic.rstrip()))
    is_exist = searchExactWikiItem(capitaliseFirstLetter(topic.rstrip()))
    if(not search_result and not is_exist):
        """checking for the alias name of the topic if it exists or not"""
        is_alias_exist = getItemByAlias(capitaliseFirstLetter(topic.rstrip()))
        if (not is_alias_exist):
            """" creating topic if there is none already """
            data = {}
            label = {lang: topic.capitalize().strip()}
            description = {lang: topic.capitalize().strip() + "entity"}
            data['labels'] = label
            data['descriptions'] = description
            topic_entity = pywikibot.ItemPage(wikibase_repo)
            topic_entity.editEntity(data, summary='Creating new item')
        else:
            """getting the topic by alias"""
            topic_entity = getItemByAlias(
                capitaliseFirstLetter(topic.rstrip()))
            topic_entity.get()

    else:
        topic_entity = getItemByAlias(capitaliseFirstLetter(topic.rstrip()))
        topic_entity.get()

    if (topic_entity):
        """ mentioned in """
        mentioned_in_property = pywikibot.PropertyPage(
            wikibase_repo, ProductionConfig.MENTIONED_IN_PROPERTY_PID)
        mentioned_in_property.get()
        mentioned_in_claim = pywikibot.Claim(
            wikibase_repo, mentioned_in_property.id, datatype=mentioned_in_property.Type)
        paragraph_entity.get()
        mentioned_in_claim.setTarget(paragraph_entity)
        topic_entity.addClaim(mentioned_in_claim,
                                summary='Adding new claim')
        return topic_entity

    else:
        return False

def createParagraphEntity(label, description, text, document_entity, sub_topics, lang):

    data = {}
    print(f'inserting paragraph entity')
    data['labels'] = label
    data['descriptions'] = description
    paragraph_item = pywikibot.ItemPage(wikibase_repo)
    paragraph_item.editEntity(data, summary='Creating new item')

    """
    instance of
    """
    paragraph_class_entity = pywikibot.ItemPage(
        wikibase_repo, f'{ProductionConfig.PARAGRAPH_CLASS_QID}')
    paragraph_class_entity.get()
    instance_of_property = pywikibot.PropertyPage(wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
    instance_of_property.get()
    instance_claim = pywikibot.Claim(wikibase_repo, instance_of_property.id, datatype=instance_of_property.Type)
    instance_claim.setTarget(paragraph_class_entity)
    paragraph_item.addClaim(
        instance_claim, summary='Adding claim to the paragraph')

    """
    part of
    """
    part_of_property = pywikibot.PropertyPage(wikibase_repo, f'{ProductionConfig.PART_OF_PROPERTY_PID}')
    part_of_property.get()
    part_of_claim = pywikibot.Claim(wikibase_repo, part_of_property.id, datatype=part_of_property.Type)
    part_of_claim.setTarget(document_entity)
    paragraph_item.addClaim(
        part_of_claim, summary='Adding claim to the paragraph')

    """
    has text
    """

    has_text_property = pywikibot.PropertyPage(wikibase_repo, f'{ProductionConfig.HAS_TEXT_PROPERTY_PID}')
    has_text_property.get()
    has_text_claim = pywikibot.Claim(wikibase_repo, has_text_property.id, datatype=has_text_property.Type)
    has_text_claim.setTarget(text)
    paragraph_item.addClaim(
        has_text_claim, summary='Adding claim to the paragraph')

    if (paragraph_item):

        """ for sub topics """
        for sub_topic in sub_topics:
            topic_entity = create_sub_topic(sub_topic.label, paragraph_item, document_entity, lang)
            topic_entity.get()

            if (topic_entity):
                has_topic_property = pywikibot.PropertyPage(wikibase_repo, f'{ProductionConfig.HAS_TOPIC_PROPERTY_PID}')
                has_topic_property.get()
                has_topic_claim = pywikibot.Claim(wikibase_repo, has_topic_property.id, datatype=has_topic_property.Type)
                has_topic_claim.setTarget(topic_entity)
                paragraph_item.addClaim(
                    has_topic_claim, summary='Adding claim to the paragraph')

        has_paragraph_property = pywikibot.PropertyPage(wikibase_repo, f'{ProductionConfig.HAS_PARAGRAPH_PROPERTY_PID}')
        has_paragraph_property.get()
        has_paragraph_claim = pywikibot.Claim(wikibase_repo, has_paragraph_property.id, datatype=has_paragraph_property.Type)
        has_paragraph_claim.setTarget(paragraph_item)
        document_entity.addClaim(
            has_paragraph_claim, summary='Adding caim to the document')

        return paragraph_item

    else:
        return False


def Upload2Wikibase(filePath):
    document_name = ntpath.basename(filePath)[0:-4]
    label = {}
    data = {}
    language_code = 'en'
    label = {language_code : document_name.capitalize()}
    description_text = "This document titled " + document_name + " and is added to the disability wikibase"
    description = {language_code: description_text}

    wiki_doc_item = createDocumentEntity(label=label, description=description, key = document_name)
    # if (not wiki_doc_item):
    #     return False
    print('hi-1')
    with open(filePath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        line_count = 0
        print('hi-2')
        for line in csv_reader:
            print(f'currently on the line {line_count}')
            try:
                paragraph_label_value =  f"{document_name.capitalize()} paragraph number {line_count}"
                paragraph_description_value =  f"Paragraph from {document_name.capitalize()} document"
                paragraph_label = {language_code : paragraph_label_value}
                paragraph_description = {language_code : paragraph_description_value}
                paragraph_text_value = line['Paragraph']
                paragraph_text = {language_code : paragraph_text_value}
                paragraph_topics = []
                for i in range(1, 15):
                    if(line[f'Label {i}']) != "":
                        paragraph_topics.append(line[f'Label {i}'].capitalize())
                    else:
                        pass
                paragraph_subtopics = {language_code : paragraph_topics}

                paragraph_entity = createParagraphEntity(label = paragraph_label, description = paragraph_description, text = paragraph_text, document_entity= wiki_doc_item , sub_topics= paragraph_subtopics, lang = language_code)
                paragraph_entity.get()
                print('This is paragraph subtopics,', paragraph_subtopics)
                print('This is paragraph text', paragraph_text)
                print('hi-3')
            except Exception as e:
                print('The exception encountered is ', e)
            line_count = line_count + 1
    print('hi-4')

def main():
    Upload2Wikibase("data/Black-Disability/CSV/(1977) The Combahee River Collective Statement.csv")


if __name__ == '__main__':
    main()
