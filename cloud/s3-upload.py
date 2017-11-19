import boto3
import time
from credentials import AWS_KEY, AWS_SECRET, REGION

BUCKET = "iot-smart-hedgehog-home-bucket"

s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET)
                            

filenameWithPath = "./pygmy_hedgehogs_test.jpg"                            
path_filename='pygmy_hedgehogs_test.jpg'

s3.upload_file(filenameWithPath, BUCKET, path_filename)
s3.put_object_acl(ACL='public-read', Bucket=BUCKET, Key=path_filename)