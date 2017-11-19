from awscredentials import ACCESS_KEY, SECRET_KEY, REGION
import boto3
import time
import json

sqs = boto3.resource('sqs', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION)
                            
# Get the queue
queue = sqs.get_queue_by_name(QueueName='TestA')


# Get the table
dynamodb = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY,
                            region_name=REGION)

Students = dynamodb.Table('Students');
Courses = dynamodb.Table('Courses');
Takes = dynamodb.Table('Takes');
Grades = dynamodb.Table('Grades');

def writeToDynamoDB(data):
    if data['table'] == 'Students':
        print('Students')
        Students.put_item(Item=data)
    elif data['table'] == 'Courses':
        print('Courses')
        Courses.put_item(Item=data)
    elif data['table'] == 'Grades':
        print('Grades')
        Grades.put_item(Item=data)
    else:
        print('Takes')
        Takes.put_item(Item=data)

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        data = message.body
        print message.body
        writeToDynamoDB(json.loads(message.body))
        message.delete()
    	time.sleep(1)


