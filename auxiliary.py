import pymongo
import os
from openai import OpenAI

EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MONGO_DB_CONNECTION_URL = os.environ.get('MONGO_DB_CONNECTION_URL')
def connect_openai():
    openai_client = OpenAI(    
        api_key=OPENAI_API_KEY
    )

    return openai_client

def generate_embedding(openai_client):
    response = openai_client.embeddings.create(
                    input="How do I score for the end of the game?",
                    model=EMBEDDING_MODEL
                )
    embedding = response.data[0].embedding
    return embedding

def generate_response(openai_client):
    return None 

def connectClient():
    # Create a new client and connect to the server
    client = MongoClient(MONGO_DB_CONNECTION_URL)
    # Send a ping to confirm a successful connection
    return client

def connectDatabase(client, databaseName):
    return client[databaseName]

def connectCollection(database, collectionName):
    return database[collectionName]

def fetch_from_mongo(database, embedding):
    pipeline = [
    {
        '$vectorSearch': {
            'index': 'bg_embedding_search', 
            'path': 'rule_embedding', 
            'queryVector': embedding, 
            'numCandidates': 150, 
            'filter': { "name": { "$eq": "cascadia" }, },
            'limit': 3
        }
    }, 
    {
        '$project': {
            '_id': 0, 
            'rule_description': 1, 
            'image_path': 1, 
            'score': {
                '$meta': 'vectorSearchScore'
            }
        }
    }
    ]
    
    return database.aggregate(pipeline)

