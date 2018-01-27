# IoT Smart Hedgehog Home
### Check out our Mbed Notebook Site with some demo videos!
https://os.mbed.com/users/albertoli/notebook/iot_smart_hedgehog_home/

### Brief Description
A hedgehog smart house that will allow users to monitor their hedgehog remotely. The smart environment will allow health monitoring features for the hedgehog to be autonomously driven by data collected from a range of sensors. The sensory feedback data provided from the smart environment will be uploaded to a cloud through Amazon Web Services (AWS) and stored in a cloud Relational Database Service (RDS). 

The user will be able to interface with the smart environment through a web interface. It will allow for the user to monitor the status of the hedgehog by looking at graphs of certain metrics such as amount of time the hedgehog runs on the wheel and the temperature of his environment in a dashboard interface.

![Alt text](img/architecture_model.png?raw=true "Architecture Model")

Typical hardware and sensors we would look to include are:
Camera to get a snapshot of what is happening inside the cage at a given time Related hardware: PI camera
Temperature - This will be sent to the cloud, logged, and displayed in a graph. Related hardware: TMP36 temperature sensor
Sounds - This will allow for the ability to emulate sounds native to its habitat. It will also allow for the ability to play sounds that can calm the hedgehog down or stimulate it, depending on the amount of motion recorded per day for it to be in a healthy physical state. Related hardware: Class D amp, speaker (in MBED kit) , potentiometer (for manual volume control)
Wheel/rotation sensor - this could be used to calculate how much the hedgehogs are running Related hardware: Magnet and reed switch/ hall effect sensor 
Automatic/ Timed food dispenser- used to give out food during the specified feeding time. Related hardware: Servo

![Alt text](img/features_model2.png?raw=true "Features Model")
Main microcontroller is planned to be the PI while utilizing WIFI for networking. It will push sensor readings to the AWS endpoint Python and the Boto3 library. It will also be the main interface for the camera. An MBED will be used for the other sensors, and will push readings to the PI as necessary. 

The enclosure will be a proof of concept build, just utilizing a box or a set of wire-mesh cage pieces. 

