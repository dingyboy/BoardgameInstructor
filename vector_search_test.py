import pymongo
import os
from openai import OpenAI

# connect to your Atlas cluster

uri = os.environ.get('MONGO_DB_CONNECTION_URL')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL')

client = pymongo.MongoClient(uri)
def connect_openai():
    openai_client = OpenAI(    
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    return openai_client

def generate_embedding(openai_client):
  response = openai_client.embeddings.create(
                    input="How do I score for the end of the game?",
                    model=EMBEDDING_MODEL
                )
  embedding = response.data[0].embedding
  return embedding
# define pipeline

def create_pipeline(embedding): 
  pipeline = [
  {
    '$vectorSearch': {
      'index': 'bg_embedding_search', 
      'path': 'rule_embedding', 
      'queryVector': embedding, 
      'numCandidates': 150, 
      'filter': { "name": { "$eq": "cascadia" }, },
      'limit': 20
    }
  }, {
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
  return pipeline

openai_client = connect_openai()
embedding = generate_embedding(openai_client)
pipeline = create_pipeline(embedding)
# run pipeline
result = client["BoardgameInstructions"]["BGInstruct"].aggregate(pipeline)

# print results
for i in result:
    print(i)
