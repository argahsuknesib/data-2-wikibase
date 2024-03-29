from cgitb import text
import csv
import configparser
from fileinput import filename
import ntpath
from pydoc import doc
import sys
import traceback
import time
from urllib import request
from xml.dom.minidom import Document
import pywikibot
from SPARQLWrapper import SPARQLWrapper, JSON
from configWikibaseID import ProductionConfig
import re
from glossaryList import WordList

config = configparser.ConfigParser()
config.read('config/application.config.ini')

wikibase = pywikibot.Site("my", "my")
sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
site = pywikibot.Site()

wikidata = pywikibot.Site("wikidata", "wikidata")


class UploadLabels():
    def __init__(self, wikibase):
        self.wikibase = wikibase
        self.wikibase_repo = wikibase.data_repository()
        self.sparql = SPARQLWrapper(config.get('wikibase', 'sparqlEndPoint'))
        self.class_entities = {}
        self.properties = {}
        self.pywikibot = pywikibot

    def capitaliseFirstLetter(self, word):
        return word.capitalize()

    def searchItem(self, label):
        if label is None:
            return False
        params = {'action': 'wbsearchentities', 'format': 'json',
                  'language': 'en', 'type': 'item', 'limit': 100, 'search': label}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        return result

    def searchExactWikiItem(self, label):
        if label is None:
            return True
        params = {'action': 'wbsearchentities', 'format': 'json',
                  'language': 'en', 'type': 'item', 'limit': 1, 'search': label}
        request = self.wikibase._simple_request(**params)
        result = request.submit()
        print(result)
        if (len(result['search']) > 0):
            for item in result['search']:
                if (item.get('label') == label):
                    return True
        return False

    def searchWikiItem(self, label):
        query = """
            select ?label ?s where 
            {
                ?s ?p ?o.
                ?s rdfs:label ?label .
                FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
                FILTER(?label = '"""+label+"""'@en)
            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        if (len(results['results']['bindings']) > 0):
            return True
        else:
            return False

    def getWikiItem(self, label):
        query = """
            select ?label ?s where 
            {
                ?s ?p ?o;
                ?s rdfs:label ?label .
                FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
                FILTER(?label = '"""+label+"""'@en)

            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        item_qid = results['results']['bindings'][0]['s']['value'].split(
            "/")[-1]
        return item_qid

    def searchItemByAlias(self, label):
        query = """
            SELECT DISTINCT ?s ?label where
            {
                ?s ?p ?o;
                    skos:altLabel ?label .
                FILTER(lang(?label)='fr' || lang(?label)='en')
                FILTER(?label = '"""+label+"""'@en)
            }
        
        """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        if (len(results['results']['bindings']) > 0):
            return True
        else:
            return False

    def getItemBySparql(self, label):
        query = """
        
            select ?label ?s where
            {
                ?s ?p ?o.
                ?s rdfs:label ?label.
                FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
                FILTER(?label = '"""+label+"""'@en)
                
            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        if (results.get('results', None) is not None and
            results.get('results').get('bindings') is not None and
            type(results.get('results').get('bindings')) is list and
            len(results.get('results').get('bindings')) > 0 and
            results.get('results').get('bindings')[0] is not None and
            results.get('results').get('bindings')[0].get('s', None) is not None and
            results.get('results').get('bindings')[0].get(
            's').get('value', None) is not None
            ):
            item_qid = results['results']['bindings'][0]['s']['value'].split(
                "/")[-1]
            if (item_qid):
                item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
                return item
            else:
                print('false from getItemBySparql - first')
                return False
        else:
            print('false from getItemBySparql  - second')
            return False

    def getItemByAlias(self, label):
        query = """
        
            SELECT DISTINCT ?label ?s where 
            {
                ?s ?p ?o;
                skos:altLabel ?label.
                FILTER(lang(?label) = 'fr' || lang(?label) = 'en')
                FILTER(?label = '""" + label + """'@en)
            }
        """

        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

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
                item = self.pywikibot.ItemPage(self.wikibase_repo, item_qid)
                return item
            else:
                print('false from getItemByAlias')
                return False
        else:
            print('false from getItemByAlias')
            return False

    def createDocumentEntity(self, label, description, key):
        search_result = self.searchWikiItem(
            self.capitaliseFirstLetter(key.rstrip()))
        is_exist = self.searchExactWikiItem(
            self.capitaliseFirstLetter(key.rstrip()))

        if (not search_result and not is_exist):
            data = {}
            print(f'inserting document entity {key.rstrip()}')
            data['labels'] = label
            data['descriptions'] = description
            new_item = self.pywikibot.ItemPage(self.wikibase_repo)
            new_item.editEntity(data, summary='Creating new item')

            new_claims = []
            claim_data = {}

            instance_claim = {}
            document_class_entity = self.pywikibot.ItemPage(
                self.wikibase_repo, f'{ProductionConfig.DOCUMENT_CLASS_QID}')
            document_class_entity.get()
            instance_of_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
            instance_of_property.get()
            instance_claim = self.pywikibot.Claim(
                self.wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
            instance_claim.setTarget(document_class_entity)

            """
            uncomment this code about document URI just in case you 
            found a reason to add the actual link of the document.
            """

            new_claims.append(instance_claim.toJSON())
            claim_data['claims'] = new_claims
            new_item.editEntity(claim_data, summary='Adding new claims')

            return new_item
        else:
            entity = self.getItemBySparql(
                self.capitaliseFirstLetter(key.rstrip()))
            return entity

    
    def createTitleWordsEntity(self, document_entity,  title_word, lang):  

        title_entity = {}
        search_result = self.searchWikiItem(self.capitaliseFirstLetter(title_word.rstrip()))
        is_exist = self.searchExactWikiItem(self.capitaliseFirstLetter(title_word.rstrip()))
        is_alias_exist = self.searchItemByAlias(self.capitaliseFirstLetter(title_word.rstrip()))   

        if (not search_result and not is_exist):
            if(not is_alias_exist):
                data = {}
                label = {lang: title_word.capitalize().strip()}
                description = {lang: title_word.capitalize().strip() + " entity and should be added into the glossary."}
                data['labels'] = label
                data['description'] = description
                title_entity = self.pywikibot.ItemPage(self.wikibase_repo)
                title_entity.editEntity(data, summary='creating a new title word item')
            else:
                title_entity = self.getItemByAlias(self.capitaliseFirstLetter(title_word.rstrip()))
        else:
            title_entity = self.getItemBySparql(self.capitaliseFirstLetter(title_word.rstrip()))
            title_entity.get()


        if (title_entity):
            has_title_word_property = self.pywikibot.PropertyPage(self.wikibase_repo, f'{ProductionConfig.HAS_TITLE_WORDS_PID}')
            has_title_word_property.get()
            has_title_word_claim = self.pywikibot.Claim(self.wikibase_repo, has_title_word_property.id)
            document_entity.get()
            has_title_word_claim.setTarget(document_entity)
            title_entity.addClaim(has_title_word_claim, summary="adding new claim")

    

    def create_sub_topic(self, topic, paragraph_entity, document_entity, lang):
        topic_entity = {}
        search_result = self.searchWikiItem(
            self.capitaliseFirstLetter(topic.rstrip()))
        is_exist = self.searchExactWikiItem(
            self.capitaliseFirstLetter(topic.rstrip()))
        is_alias_exist = self.searchItemByAlias(
            self.capitaliseFirstLetter(topic.rstrip()))

        if (not search_result and not is_exist):
            if(not is_alias_exist):
                data = {}
                label = {lang: topic.capitalize().strip()}
                description = {lang: topic.capitalize().strip() + " entity"}
                data['labels'] = label
                data['description'] = description
                topic_entity = self.pywikibot.ItemPage(self.wikibase_repo)
                topic_entity.editEntity(data, summary='Creating new item')
            else:
                topic_entity = self.getItemByAlias(
                    self.capitaliseFirstLetter(topic.rstrip()))
        else:
            topic_entity = self.getItemBySparql(
                self.capitaliseFirstLetter(topic.rstrip()))
            topic_entity.get()

        if (topic_entity):
            """ mentioned in claim """
            mentioned_in_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, f'{ProductionConfig.MENTIONED_IN_PROPERTY_PID}')
            mentioned_in_property.get()
            mentioned_in_claim = self.pywikibot.Claim(
                self.wikibase_repo, mentioned_in_property.id)
            paragraph_entity.get()
            mentioned_in_claim.setTarget(paragraph_entity)
            topic_entity.addClaim(mentioned_in_claim,
                                  summary="adding new claim")

            return topic_entity
        else:
            return False

    def createParagraphEntity(self, label, description, text, document_entity, sub_topics, lang):

        data = {}
        print(f'inserting paragraph entity')
        data['labels'] = label
        data['descriptions'] = description
        paragraph_item = self.pywikibot.ItemPage(self.wikibase_repo)
        paragraph_item.editEntity(data, summary='Creating new item')

        """
        instance of
        """
        paragraph_class_entity = self.pywikibot.ItemPage(
            self.wikibase_repo, f'{ProductionConfig.PARAGRAPH_CLASS_QID}')
        paragraph_class_entity.get()
        instance_of_property = self.pywikibot.PropertyPage(
            self.wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
        instance_of_property.get()
        instance_claim = self.pywikibot.Claim(
            self.wikibase_repo, f'{ProductionConfig.INSTACE_OF_PROPERTY_PID}')
        instance_claim.setTarget(paragraph_class_entity)
        paragraph_item.addClaim(
            instance_claim, summary='Adding claim to the paragraph')

        """
        part of
        """
        part_of_property = self.pywikibot.PropertyPage(
            self.wikibase_repo, f'{ProductionConfig.PART_OF_DOCUMENT_PROPERTY_PID}')
        part_of_property.get()
        part_of_claim = self.pywikibot.Claim(
            self.wikibase_repo, part_of_property.id)
        part_of_claim.setTarget(document_entity)
        paragraph_item.addClaim(
            part_of_claim, summary='Adding claim to the paragraph')

        """
        has text
        """

        has_text_property = self.pywikibot.PropertyPage(
            self.wikibase_repo, f'{ProductionConfig.HAS_TEXT_PROPERTY_PID}')
        has_text_property.get()
        has_text_claim = self.pywikibot.Claim(
            self.wikibase_repo, has_text_property.id)
        has_text_claim.setTarget(text.strip())
        paragraph_item.addClaim(
            has_text_claim, summary='Adding claim to the paragraph')

        if (paragraph_item):

            """ for sub topics """
            for sub_topic in sub_topics:
                topic_entity = self.create_sub_topic(
                    sub_topic, paragraph_item, document_entity, lang)
                topic_entity.get()

                if (topic_entity):
                    has_topic_property = self.pywikibot.PropertyPage(
                        self.wikibase_repo, f'{ProductionConfig.HAS_TOPIC_PROPERTY_PID}')
                    has_topic_property.get()
                    has_topic_claim = self.pywikibot.Claim(
                        self.wikibase_repo, has_topic_property.id)
                    has_topic_claim.setTarget(topic_entity)
                    paragraph_item.addClaim(
                        has_topic_claim, summary='Adding claim to the paragraph')

            has_paragraph_property = self.pywikibot.PropertyPage(
                self.wikibase_repo, f'{ProductionConfig.HAS_PARAGRAPH_PROPERTY_PID}')
            has_paragraph_property.get()
            has_paragraph_claim = self.pywikibot.Claim(
                self.wikibase_repo, has_paragraph_property.id)
            has_paragraph_claim.setTarget(paragraph_item)
            document_entity.addClaim(
                has_paragraph_claim, summary='Adding claim to the document')

            return paragraph_item

        else:
            return False

    def Upload2Wikibase(self, filePath):
        document_name = ntpath.basename(filePath)[0:-4]
        language_code = 'en'
        label = {language_code: document_name.capitalize()}
        description_text = "This document titled " + \
            document_name + " and is added to the disability wikibase"
        description = {language_code: description_text}

        wiki_doc_item = self.createDocumentEntity(
            label=label, description=description, key=document_name)

        '''
        add the has title words entity here
        '''
        glossary_list = WordList()
        word_list = []
        word_document_name = document_name.split()
        for word in word_document_name:
            if word.capitalize() in glossary_list:
                word_list.append(word)
            else:
                pass
        
        for glossary_word in word_list:
            title_word_entity = self.createTitleWordsEntity(document_entity=wiki_doc_item, title_word=glossary_word, lang=language_code)
            title_word_entity.get()

        with open(filePath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 1
            for line in csv_reader:
                print(f'currently on the line {line_count}')
                try:
                    paragraph_label_value = f"{document_name.capitalize()} paragraph number {line_count}"
                    paragraph_description_value = f"Paragraph from {document_name.capitalize()} document"
                    paragraph_label = {language_code: paragraph_label_value}
                    paragraph_description = {
                        language_code: paragraph_description_value}
                    paragraph_text_raw = line['Paragraph'].strip()

                    paragraph_text = paragraph_text_raw.replace('\n', ' ').replace(
                        '\t', ' ').replace('\r', ' ').rstrip().lstrip()
                    paragraph_topics = []
                    for i in range(1, 15):
                        if(line[f'Label {i}']) != "":
                            paragraph_topics.append(
                                line[f'Label {i}'].capitalize())
                        else:
                            pass
                    paragraph_subtopics = paragraph_topics

                    paragraph_entity = self.createParagraphEntity(label=paragraph_label, description=paragraph_description,
                                                                  text=paragraph_text, document_entity=wiki_doc_item, sub_topics=paragraph_subtopics, lang=language_code)
                    time.sleep(5)
                except Exception as e:
                    print('The exception encountered is ', e)

                line_count = line_count + 1
                time.sleep(5)


def main():
    uploadingLabels = UploadLabels(wikibase)
    #uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/(1977) The Combahee River Collective Statement.csv")
    #uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/A Paradoxical History of Black Disease by Cyrée Jarelle Johnson.csv")
    #uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Autistic while black How autism amplifies stereotypes by Catina Burkett.csv")
    #uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Black Disability Gone Viral word.csv")
    #uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Developing and Reflecting on a Black Disability Studies Pedagogy .csv")
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Disability Justice Is an Essential Part of Abolishing Police and Prisons by Talila _TL_ Lewis.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/END THE WAR ON BLACK HEALTH AND BLACK DISABLED PEOPLE report word.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/For Disabled Sex Workers, Congress Anti-Trafficking Legislation Is Life Threatening by Cyrée Jarelle Johnson.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/How I Relate to the DAPL Protests as a Black Woman by Keah Brown.csv")
    time.sleep(5) 
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Integrating Race word.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Introducing White Disability Studies word.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Magic from the madness- On black disabled activists and artists making change in 2016 by Syrus Marcus Ware.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Our language is the heart of what we are- Tamyka Bullen is putting deaf culture centre stage.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/The Prison Strike Challenges Ableism and Defends Disability Rights by Talila A. Lewis & Dustin Gibson.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/The Roots of Krip-Hop Nation Rob, Keith & Leroy by von koka.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/They Dont Know, Dont Show, or Dont Care_Autisms White Privilege Problem by Morénike Giwa Onaiwu.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Understanding the Policing of Black, Disabled Bodies by Vilissa Thompson.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/What Disabled Culture Teaches On Life Post word.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/White Privilege & Inspiration Porn by Vilissa Thompson.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/why I dons use _anti-Black ableism_ (& language longings) by Talila A. Lewis.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Work in the INtersection- A Black Feminist Disability Framework by Moya Bailey and Izetta Autumn Mobley.csv")
    time.sleep(5)
    uploadingLabels.Upload2Wikibase("data/Black-Disability/CSV/Working definition of ableism word.csv")
    #uploadingLabels.Upload2Wikibase("")
    #uploadingLabels.Upload2Wikibase("")


if __name__ == '__main__':
    main()
