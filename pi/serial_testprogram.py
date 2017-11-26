import time
import serial
import boto3
from credentials import AWS_KEY, AWS_SECRET, REGION

sqs = boto3.resource('sqs', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)
queue = sqs.get_queue_by_name(QueueName='PiQueue')
out= ""                            
# configure the serial connections (the parameters differs on the device you are connecting to)
# Get the queue
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        data = message.body
        print message.body
        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########
        if (data[0] == "Music"):
            subprocess.call(["sudo echo","m >",  "/dev/ttyACM0"])
        elif (data[0] == "Snack"):
            subprocess.call(["sudo echo", "t >", "/dev/ttyACM0"])
        


