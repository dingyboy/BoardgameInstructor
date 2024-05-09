
from pymongo.mongo_client import MongoClient
import os

def connectClient():
    uri = os.environ.get('MONGO_DB_CONNECTION_URL')
    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    return client

def pingClient(client):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def connectDatabase(client, databaseName):
    return client[databaseName]

def connectCollection(database, collectionName):
    return database[collectionName]

def insertItems(collection, items):
    try:
        collection.insert_many(items)
        print("Successfully inserted items.")
    except Exception as e:
        print(e)    



item_1 = {
  "_id" : "U1IT00001",
  "item_name" : "Blender",
  "max_discount" : "10%",
  "batch_number" : "RR450020FRG",
  "price" : 340,
  "category" : "kitchen appliance"
}

item_2 = {
  "_id" : "U1IT00002",
  "item_name" : "Egg",
  "category" : "food",
  "quantity" : 12,
  "price" : 36,
  "item_description" : "brown country eggs"
}
# client = connectClient()
# pingClient(client)
# db = connectDatabase(client, 'BoardgameInstructions')
# collection = connectCollection(db, 'BGInstruct')
# insertItems(collection, [item_1, item_2])

