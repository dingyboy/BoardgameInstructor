import boto3
import os

ACCESS_ID = os.environ.get("AWS_ACCESS_ID")

AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")



client = boto3.client('s3', region_name='us-east-2',              
        aws_access_key_id=ACCESS_ID,
         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
response = client.list_buckets()
# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

# client.upload_file('./boardgame_asset/railroad_ink/railroad_ink_page0.jpg', 'bg-instructor-rule-storage','railroad_ink_page0.jpg')

