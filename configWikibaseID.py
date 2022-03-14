import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    # DEBUG = False
    # MAIN_PATH = basedir
    # UPLOAD_FOLDER = './resources/uploads'
    # TEMP_DOC_FOLDER = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
    #     0]+'\\resources\\temp_doc'
    # ORIGINAL_FILE_FOLDER = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
    #     0]+'\\resources\\uploads'
    # RESULT_FOLDER = './resources/classified/result'
    # CLASSIFIER_MODEL = './resources/classifier_model'
    # UPLOAD_WIKIEDIT_REQUEST_FOLDER = './resources/classified/requested'
    # UPLOAD_COMPLETED_FOLDER = './resources/classified/completed'
    # BCRYPT_LOG_ROUNDS = 6
    # # MESSAGE BROKER
    # REDIS_SERVER = 'redis://localhost:6379'
    # MESSAGING_SERVICE_HOST = 'localhost'

    # # PYWIKICONFIGURATION
    # PYWIKI_FAMILY_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
    #     0]+'\\config\\my_family.py'
    # PYWIKI_USER_PASSWORD_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
    #     0]+'\\user-password.py'
    # WIKI_USER_NAME = 'WikibaseAdmin'
    # WIKI_BOT_USER_NAME = 'bot_user_1'
    # WIKI_BOT_SECRET = 'cicb8eb65ktd956a0b43vauc4o63fpak'
    # WIKI_SPARQL_END_POINT = 'http://localhost:8989/bigdata/namespace/wdq/sparql'
    # WIKI_DOMAIN = 'localhost:8181'
    # WIKI_PROTOCOL = 'http'
    # WIKI_API_URI = 'http://localhost:8181/w/api.php'

    # # ERROR LOG
    # ERROR_LOG_FILE = './resources/error_log/debug_error.txt'

    # # WIKIBASE PROPERTIES
    # DOCUMENT_CLASS_QID = 'Q1'
    # WEB_CONTENT_CLASS_QID = 'Q3'
    # PARAGRAPH_CLASS_QID = 'Q5'
    # TOPIC_CLASS_QID = 'Q4'
    # INSTACE_OF_PROPERTY_PID = 'P29'
    # DOCUMENT_REFERENCE_URI_PROPERTY_PID = 'P31'
    # PART_OF_DOCUMENT_PROPERTY_PID = 'P33'
    # HAS_TEXT_PROPERTY_PID = 'P23'
    # HAS_TOPIC_PROPERTY_PID = 'P3'
    # HAS_PARAGRAPH_PROPERTY_PID = 'P32'
    # MENTIONED_IN_PROPERTY_PID = 'P25'

    # UBUNTU FORMAT************************************************************
    # SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    # DEBUG = False
    # MAIN_PATH = basedir
    # UPLOAD_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/resources/uploads'
    # TEMP_DOC_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/resources/temp_doc'
    # ORIGINAL_FILE_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/resources/uploads'
    # RESULT_FOLDER = './resources/classified/result'
    # CLASSIFIER_MODEL = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/resources/classifier_model'
    # UPLOAD_WIKIEDIT_REQUEST_FOLDER = './resources/classified/requested'
    # UPLOAD_COMPLETED_FOLDER = './resources/classified/completed'
    # BCRYPT_LOG_ROUNDS = 6

    # # MESSAGE BROKER
    # REDIS_SERVER = 'redis://localhost:6379'
    # MESSAGING_SERVICE_HOST = 'localhost'

    # # PYWIKICONFIGURATION
    # PYWIKI_FAMILY_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/config/my_family.py'
    # PYWIKI_USER_PASSWORD_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/user-password.py'
    # WIKI_USER_NAME = 'WikibaseAdmin'
    # WIKI_BOT_USER_NAME = 'bot_user_1'
    # WIKI_BOT_SECRET = 'cicb8eb65ktd956a0b43vauc4o63fpak'
    # WIKI_SPARQL_END_POINT = 'http://localhost:8989/bigdata/namespace/wdq/sparql'
    # WIKI_DOMAIN = 'localhost:8181'
    # WIKI_PROTOCOL = 'http'
    # WIKI_API_URI = 'http://localhost:8181/w/api.php'

    # # ERROR LOG
    # ERROR_LOG_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
    #     0]+'/resources/error_log/debug_error.txt'

    # # WIKIBASE PROPERTIES
    # DOCUMENT_CLASS_QID = 'Q1'
    # WEB_CONTENT_CLASS_QID = 'Q1'
    # PARAGRAPH_CLASS_QID = 'Q183'
    # TOPIC_CLASS_QID = 'Q2'
    # INSTACE_OF_PROPERTY_PID = 'P1'
    # DOCUMENT_REFERENCE_URI_PROPERTY_PID = 'P32'
    # PART_OF_DOCUMENT_PROPERTY_PID = 'P33'
    # HAS_TEXT_PROPERTY_PID = 'P24'
    # HAS_TOPIC_PROPERTY_PID = 'P4'
    # HAS_PARAGRAPH_PROPERTY_PID = 'P34'
    # MENTIONED_IN_PROPERTY_PID = 'P26'


class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1/dis_wiki"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # DEV CONFIG
    DEBUG = False
    MAIN_PATH = basedir
    UPLOAD_FOLDER = './resources/uploads'
    TEMP_DOC_FOLDER = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\resources\\temp_doc'
    ORIGINAL_FILE_FOLDER = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\resources\\uploads'
    RESULT_FOLDER = './resources/classified/result'
    CLASSIFIER_MODEL = './resources/classifier_model'
    UPLOAD_WIKIEDIT_REQUEST_FOLDER = './resources/classified/requested'
    UPLOAD_COMPLETED_FOLDER = './resources/classified/completed'
    BCRYPT_LOG_ROUNDS = 6
    # MESSAGE BROKER
    REDIS_SERVER = 'redis://localhost:6379'
    MESSAGING_SERVICE_HOST = 'localhost'

    # PYWIKICONFIGURATION
    PYWIKI_FAMILY_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\config\\my_family.py'
    PYWIKI_USER_PASSWORD_FILE = basedir.rsplit('\\', 1)[0].rsplit('\\', 1)[
        0]+'\\user-password.py'
    WIKI_USER_NAME = 'WikibaseAdmin'
    WIKI_BOT_USER_NAME = 'bot_user_1'
    WIKI_BOT_SECRET = 'cicb8eb65ktd956a0b43vauc4o63fpak'
    WIKI_SPARQL_END_POINT = 'http://localhost:8989/bigdata/namespace/wdq/sparql'
    WIKI_DOMAIN = 'localhost:8181'
    WIKI_PROTOCOL = 'http'
    WIKI_API_URI = 'http://localhost:8181/w/api.php'

    # ERROR LOG
    ERROR_LOG_FILE = './resources/error_log/debug_error.txt'

    # WIKIBASE PROPERTIES
    DOCUMENT_CLASS_QID = 'Q2'
    WEB_CONTENT_CLASS_QID = 'Q4'
    PARAGRAPH_CLASS_QID = 'Q6'
    TOPIC_CLASS_QID = 'Q5'
    INSTACE_OF_PROPERTY_PID = 'P1'
    DOCUMENT_REFERENCE_URI_PROPERTY_PID = 'P2'
    PART_OF_DOCUMENT_PROPERTY_PID = 'P4'
    HAS_TEXT_PROPERTY_PID = 'P27'
    HAS_TOPIC_PROPERTY_PID = 'P7'
    HAS_PARAGRAPH_PROPERTY_PID = 'P3'
    MENTIONED_IN_PROPERTY_PID = 'P29'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@127.0.0.1/dis_wiki_test"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:diswikirights@127.0.0.1/dis_wiki_test"
    SQLALCHEMY_ECHO = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:diswikirights@127.0.0.1/dis_wiki"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # PROD CONFIG
    MAIN_PATH = basedir
    UPLOAD_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/resources/uploads'
    TEMP_DOC_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/resources/temp_doc'
    ORIGINAL_FILE_FOLDER = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/resources/uploads'
    RESULT_FOLDER = './resources/classified/result'
    CLASSIFIER_MODEL = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/resources/classifier_model'
    UPLOAD_WIKIEDIT_REQUEST_FOLDER = './resources/classified/requested'
    UPLOAD_COMPLETED_FOLDER = './resources/classified/completed'
    BCRYPT_LOG_ROUNDS = 6

    # MESSAGE BROKER
    REDIS_SERVER = 'redis://localhost:6379'
    MESSAGING_SERVICE_HOST = 'localhost'

    # PYWIKICONFIGURATION
    PYWIKI_FAMILY_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/config/my_family.py'
    PYWIKI_USER_PASSWORD_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/user-password.py'
    WIKI_USER_NAME = 'WikibaseAdmin'
    WIKI_BOT_USER_NAME = 'bot_user_1'
    WIKI_BOT_SECRET = 'cicb8eb65ktd956a0b43vauc4o63fpak'
    WIKI_SPARQL_END_POINT = 'http://localhost:8989/bigdata/namespace/wdq/sparql'
    WIKI_DOMAIN = 'localhost:8181'
    WIKI_PROTOCOL = 'http'
    WIKI_API_URI = 'http://localhost:8181/w/api.php'

    # ERROR LOG
    ERROR_LOG_FILE = basedir.rsplit('/', 1)[0].rsplit('/', 1)[
        0]+'/resources/error_log/debug_error.txt'

    # WIKIBASE PROPERTIES
    DOCUMENT_CLASS_QID = 'Q2'
    WEB_CONTENT_CLASS_QID = 'Q4'
    PARAGRAPH_CLASS_QID = 'Q6'
    TOPIC_CLASS_QID = 'Q5'
    INSTACE_OF_PROPERTY_PID = 'P1'
    DOCUMENT_REFERENCE_URI_PROPERTY_PID = 'P2'
    PART_OF_DOCUMENT_PROPERTY_PID = 'P4'
    HAS_TEXT_PROPERTY_PID = 'P27'
    HAS_TOPIC_PROPERTY_PID = 'P7'
    HAS_PARAGRAPH_PROPERTY_PID = 'P3'
    MENTIONED_IN_PROPERTY_PID = 'P29'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
