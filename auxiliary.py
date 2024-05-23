import pymongo
import os
from openai import OpenAI
import json
import boto3
from botocore.exceptions import ClientError


SYSTEM_PROMPT = ""
with open('./public_asset/system_prompt.json') as a:
    SYSTEM_PROMPT = json.load(a)['content']

EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

MONGO_DB_CONNECTION_URL = os.environ.get('MONGO_DB_CONNECTION_URL')
MONGO_DB_DATABASE_NAME = os.environ.get('MONGO_DB_DATABASE_NAME')
MONGO_DB_COLLECTION_NAME = os.environ.get('MONGO_DB_COLLECTION_NAME')

AWS_ACCESS_ID = os.environ.get("AWS_ACCESS_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_BG_BUCKET_NAME = os.environ.get('AWS_BG_BUCKET_NAME')
BG_ASSET_PATH = os.environ.get('BOARDGAME_ASSET_PATH')


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
        print(openai_client, model_option, prompt)
        openai_response = openai_client.chat.completions.create(
            model=model_option,
            messages= [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,

        )

        return openai_response 
    except Exception as e:
        print(e)

def request_with_image_response(openai_client, model_option, prompt, image_url):
    try:
        openai_response = openai_client.chat.completions.create(
            model=model_option,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},

                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {'url': image_url }
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return openai_response 
    except Exception as e:
        print("error here?")
        print(e)

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
            'index': 'vector_index', 
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


def connect_bucket():
    try: 
        client = boto3.client('s3', region_name='us-east-2',              
                                aws_access_key_id=AWS_ACCESS_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return client
    except Exception as e:
        print(e)
        return False

def download_image(bg_name, client):
    try:
        client.download_file(AWS_BG_BUCKET_NAME, "/" + bg_name + "/" +bg_name + '_page0.jpg', "test.jpg")
    except ClientError as e:
        print(e)
    
def fetch_image_url(client, image_path, expiration=3600):
    try:
        response = client.generate_presigned_url('get_object',
                                                        Params={'Bucket': AWS_BG_BUCKET_NAME,
                                                                'Key':  image_path},
                                                        ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    # The response contains the presigned URL
    return response
