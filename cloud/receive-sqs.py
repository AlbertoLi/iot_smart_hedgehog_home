import boto3
import time
import json
from credentials import AWS_KEY, AWS_SECRET, REGION

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')


# Get the table
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
#Service Resource
s3 = boto3.client('s3', aws_access_key_id=AWS_KEY,
                        aws_secret_access_key=AWS_SECRET)

# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')
table = dynamodb.Table('SensorData') #Load Table

def writeToDynamoDB(data):
    table.put_item(
       Item={
                "Timestamp": data['timestamp'],
                "Temperature": data['temperature'],
                "Speed": data['speed'],
                "RPM": data['rpm'],
            }
        )

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        data = message.body
        print message.body
        writeToDynamoDB(json.loads(message.body))
        message.delete()
    	time.sleep(1)