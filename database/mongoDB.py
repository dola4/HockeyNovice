from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ligue_pat']
    #return db


    # URI de connexion à MongoDB Atlas
    #uri = ""
    
    # Création du client MongoDB
    #client = MongoClient(uri)

    # Accès à la base de données spécifique
    #db = client['LiguePat']

    return db
