import pymongo
import os
from openai import OpenAI
import json


SYSTEM_PROMPT = ""
with open('./public_asset/system_prompt.json') as a:
    SYSTEM_PROMPT = json.load(a)['content']

EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MONGO_DB_CONNECTION_URL = os.environ.get('MONGO_DB_CONNECTION_URL')
MONGO_DB_DATABASE_NAME = os.environ.get('MONGO_DB_DATABASE_NAME')
MONGO_DB_COLLECTION_NAME = os.environ.get('MONGO_DB_COLLECTION_NAME')

def connect_openai():
    try: 
        openai_client = OpenAI(    
            api_key=OPENAI_API_KEY
        )

        return openai_client
    except Exception as e:
        print(e)

def generate_embedding(openai_client):
    try: 
        response = openai_client.embeddings.create(
                        input="How do I score for the end of the game?",
                        model=EMBEDDING_MODEL
                    )
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(e)

def request_response(openai_client, model_option, prompt):
    try: 
        openai_response = openai_client.chat.completions.create(
            model=model_option,
            messages= [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )

        return openai_response 
    except Exception as e:
        print(e)

def request_with_image_reponse(openai_client, modle_option, image_url):
    #Need to figure out how to incorporate the image here
    return None

def connect_mongo_client():
    try:
        # Create a new client and connect to the server
        client = pymongo.MongoClient(MONGO_DB_CONNECTION_URL)
        # Send a ping to confirm a successful connection
        return client
    except Exception as e:
        print(e)

def connect_mongo_database(client, databaseName):
    try:
        return client[databaseName]
    except Exception as e:
        print(e)

def connect_mongo_collection(database, collectionName):
    try:
        return database[collectionName]
    except Exception as e:
        print(e)

def setup_mongo_connection():
    mongo_client = connect_mongo_client()
    mongo_database = connect_mongo_database(mongo_client, MONGO_DB_DATABASE_NAME)
    mongo_collection = connect_mongo_collection(mongo_database, MONGO_DB_COLLECTION_NAME)
    return mongo_collection

def fetch_from_mongo(collection, embedding, boardgame_name):
    pipeline = [
    {
        '$vectorSearch': {
            'index': 'bg_embedding_search', 
            'path': 'rule_embedding', 
            'queryVector': embedding, 
            'numCandidates': 150, 
            'filter': { "name": { "$eq": boardgame_name }, },
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
    try:
        return collection.aggregate(pipeline)
    except Exception as e:
        print(e)

