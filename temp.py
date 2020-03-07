import csv
import time
import random
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

mqtt.Client.connected_flag=False#create flag in class
broker="192.168.1.4"
client = mqtt.Client("python1") #create new instance
client.username_pw_set(username="61b4a3be-0965-430f-bd91-25eaa250b543",password="0d896507-c2bb-4b4f-a322-4068d5ceb113")
client.on_connect=on_connect  #bind call back function
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker)      #connect to broker
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
print("in Main Loop")
client.loop_stop()    #Stop loop
# client.disconnect() # disconnect

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    message=""
    bn="Temp"
    bu="C"
    t = 0
    bt = int(time.time())
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        message = '[{"bn":"'+bn+'","v":'+str(temperature)+',"bu":"'+bu+'","bt":'+str(bt)+'},{"bn":"humidity","v":'+str(humidity)+',"bu":"RH","bt":'+str(bt)+'}]'
        client.publish("organization/2/messages",message)
        print(message)