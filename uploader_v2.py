# need to read the pdf file xx
# convert the pdf file into images xx
# read the images and convert it into text xx
# upload the images into the s3 bucket xx

# get the url for the s3 bucket xx 
# convert the text into vector search embedding xx
# upload file to mongoDB 
# need to upload image url, vectordb, and text information
import argparse

import pytesseract
from PIL import Image
import os, shutil
from pdf2image import convert_from_path
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI
from pymongo.mongo_client import MongoClient

PARENT_DIR = os.environ.get('BOARDGAME_ASSET_PATH')
ACCESS_ID = os.environ.get("AWS_ACCESS_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_BG_BUCKET_NAME = os.environ.get('AWS_BG_BUCKET_NAME')
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL')
MONGO_DB_CONNECTION_URL = os.environ.get('MONGO_DB_CONNECTION_URL')
MONGO_DB_DATBASE_NAME = os.environ.get('MONGO_DB_DATABASE_NAME')
MONGO_DB_COLLECTION_NAME = os.environ.get('MONGO_DB_COLLECTION_NAME')

# PDF to text conversion

def create_folder(bg_name='railroad_ink'):
    print("Start: create_folder " + bg_name)
    directory = bg_name
    path = os.path.join(PARENT_DIR, directory)

    try: 
        os.makedirs(path, exist_ok = True) 
        print("Directory '%s' created successfully" % directory) 
        print("Finish: create_folder " + bg_name)
        return path

    except OSError as error: 
        print("Directory '%s' can not be created" % directory)
        print("Finish: create_folder " + bg_name)

  
# Store Pdf with convert_from_path function
def convert_PDF_to_JPEG(bg_name='railroad_ink'):

    print("Start: convert_PDF_to_JPEG " + bg_name)

    images = convert_from_path(PARENT_DIR + '/' + bg_name +  '_rules.pdf')
  
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg', 'JPEG')
    print("Finish: convert_PDF_to_JPEG " + bg_name)
    return len(images)

def convert_JPEG_to_TxT(bg_name='railroad_ink'):
  
    print("Start: convert_JPEG_to_TxT " + bg_name)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    images = convert_from_path(PARENT_DIR + '/' + bg_name +  '_rules.pdf')

    for i in range(len(images)):
        rules_text = pytesseract.image_to_string(Image.open(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.jpg')).encode()
        with open(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.txt', 'wb') as f:
            f.write(rules_text)
  
    print("Finish: convert_JPEG_to_TxT " + bg_name)

# S3 Bucket Uploader
def connect_bucket():
    try: 
        s3_client = boto3.client('s3', region_name='us-east-2',              
                                aws_access_key_id=ACCESS_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return s3_client
    except Exception as e:
        print(e)
        return False

def upload_image(bg_name, client, num_images):

    path_container = []

    try: 
        for i in range(num_images):
            s3_bucket_path = "/" + bg_name + "/" +bg_name + '_page' + str(i) + '.jpg'
            path_container.append(s3_bucket_path)
            response = client.upload_file(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page' + str(i) + '.jpg', AWS_BG_BUCKET_NAME,  s3_bucket_path)
        return path_container
    except ClientError as e:
        print(e)

# Text to Vector Embedding
def connect_openai():
    openai_client = OpenAI(    
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    return openai_client

def format_data(bg_name, openai_client, path_container):
    
    mongodb_data = []
    try:
        for i in range(len(path_container)):
            f = open(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page'+ str(i) +'.txt')
            current_text = f.read()
            print("Length Check: " + bg_name + " page " + str(i) + ": " + str(len(current_text)))
            if (len(current_text) > 6000):
                # we need to do a split here where we split the page into halves until it is less than 6000
                #  FUTURE TODO for bigger boardgame rules. right now this is just whatever until later 
                print()
            else:
                # we just go ahead and do the embedding normally
                response = openai_client.embeddings.create(
                    input=current_text,
                    model=EMBEDDING_MODEL
                )
                embedding = response.data[0].embedding
                bg_data = create_data(bg_name, current_text, embedding, path_container[i], i)
                mongodb_data.append(bg_data)

        return mongodb_data
    except Exception as e:
        print(e)

def create_data(bg_name, rule_description, rule_embedding, image_path, page_number):

    mongodb_structure = {
        "name": bg_name,
        "rule_description": rule_description,
        "rule_embedding": rule_embedding,
        "image_path": image_path,
        "page_number": page_number
    }

    return mongodb_structure

# Upload file to MongoDB
def connectClient():
    # Create a new client and connect to the server
    client = MongoClient(MONGO_DB_CONNECTION_URL)
    # Send a ping to confirm a successful connection
    return client

def pingClient(client):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def connectDatabase(client):
    return client[MONGO_DB_DATBASE_NAME]

def connectCollection(database):
    return database[MONGO_DB_COLLECTION_NAME]

def insertItems(collection, items):
    try:
        collection.insert_many(items)
        print("Successfully inserted items.")
    except Exception as e:
        print(e)    

def delete_folder(bg_name='splendor'):
    shutil.rmtree(PARENT_DIR + '/' + bg_name)

def generate_asset(bg_name='cascadia'):

    print("Start: generate_asset " + bg_name)
    # Convert pdf to jpeg and
    create_folder(bg_name)
    num_images = convert_PDF_to_JPEG(bg_name)
    convert_JPEG_to_TxT(bg_name)
  
    # Uploads image to S3
    s3_client = connect_bucket()
    path_container = upload_image(bg_name, s3_client, num_images)


    # Generates Data and Vector Embedding
    openai_client = connect_openai()
    mongodb_data = format_data(bg_name, openai_client, path_container)

    # Uploads Data to MongoDB
    mongodb_client = connectClient()
    mongodb_database = connectDatabase(mongodb_client)
    mongodb_collection = connectCollection(mongodb_database)
    insertItems(mongodb_collection, mongodb_data)


    # need a delete data here to clean everything 
    delete_folder(bg_name)

    print("Finish: generate_asset " + bg_name)

parser = argparse.ArgumentParser()
parser.add_argument('--bg', type=str)
args = parser.parse_args()
generate_asset(bg_name=args.bg)

