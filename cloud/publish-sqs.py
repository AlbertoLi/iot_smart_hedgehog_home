import boto3
from credentials import AWS_KEY, AWS_SECRET, REGION
from random import randint
import time
import datetime
import json

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='SensorData')

def getData():
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    temp = randint(0,100)
    speed = randint(0,100)
    rpm = randint(50,500)
    camera = randint(0,10000)
    data = {"timestamp": timestamp, "temperature": temp, "speed": speed , "rpm": rpm}
    return data

def publish(data):
    queue.send_message(MessageBody=json.dumps(data))
    
while True:
	data = getData()
	print data
	publish(data)
	time.sleep(1)