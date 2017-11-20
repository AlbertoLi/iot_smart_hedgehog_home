import boto3
import time
import json
from credentials import AWS_KEY, AWS_SECRET, REGION

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='PiQueue')

#Service Resource
s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        data = message.body
        print message.body
        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########


        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########
        message.delete()
    	time.sleep(0.7)