import mongoengine
from mongoengine import connect,disconnect
import os

MONGO_INITDB_ROOT_USERNAME = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")

dbConfig = {
    'alias': 'core',
    'db': 'BlockChainDB',
    'username' : MONGO_INITDB_ROOT_USERNAME,
    'password' : MONGO_INITDB_ROOT_PASSWORD,
    'host' : MONGO_HOST,
    'port' : int(MONGO_PORT)
}

def globalDbInit():
    db = connect(**dbConfig)
    db.list_database_names()
    