import boto3
import os
from botocore.exceptions import ClientError
ACCESS_ID = os.environ.get("AWS_ACCESS_ID")

AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

BG_ASSET_PATH = os.environ.get('BOARDGAME_ASSET_PATH')
AWS_BG_BUCKET_NAME = os.environ.get('AWS_BG_BUCKET_NAME')


def connect_bucket():

    try: 
        client = boto3.client('s3', region_name='us-east-2',              
                                aws_access_key_id=ACCESS_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return client
    except Exception as e:
        print(e)
        return False

def upload_image(bg_name, client):

    try: 
        response = client.upload_file(BG_ASSET_PATH + '/' + bg_name + '/' + bg_name + '_page0.jpg', AWS_BG_BUCKET_NAME,  "/" + bg_name + "/" +bg_name + '_page0.jpg')
    except ClientError as e:
        print(e)

def download_image(bg_name, client):
    try:
        client.download_file(AWS_BG_BUCKET_NAME, "/" + bg_name + "/" +bg_name + '_page0.jpg', "test.jpg")
    except ClientError as e:
        print(e)
    



client = boto3.client('s3', region_name='us-east-2',              
        aws_access_key_id=ACCESS_ID,
         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
response = client.list_buckets()
# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

# upload_image('railroad_ink', client)
# download_image('railroad_ink', client)