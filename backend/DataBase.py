import mongoengine
from mongoengine import connect

dbConfig = {
    'alias': 'core',
    'db': 'BlockChainDB'
}

def globalDbInit():
    mongoengine.register_connection(**dbConfig)

def cleanDb():
    db = connect(dbConfig['db'])
    db.drop_database(dbConfig['db'])
