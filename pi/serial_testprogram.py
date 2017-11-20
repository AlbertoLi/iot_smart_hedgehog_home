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
            input = "m"
        elif (data[0] == "Snack"):
            input = "t"
        else:
            input = None

        ######## Add code here to send thru serial. Use 'data' variable which is in json form ########
        message.delete()
        time.sleep(0.7)

        if input == None:
            while ser.inWaiting() > 0:
                out += ser.read(22)

            if out != '':
                print ">>" + out
        else:
            # send the character to the device
            # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
            ser.write(input + '\r\n')
            out = ''
            # let's wait one second before reading output (let's give device time to answer)
            time.sleep(1)
            while ser.inWaiting() > 0:
                out += ser.read(22)

            if out != '':
                print ">>" + out
    if input == None:
            while ser.inWaiting() > 0:
                out += ser.read(22)

            if out != '':
                print ">>" + out


