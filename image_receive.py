import paho.mqtt.client as mqtt
import binascii
import json
from config import mqttIP, mqttPort
import time

# RPI Destination
dest = '/home/pi/images/'

# Backend Testiong
#dest = 'C:\Users\willi\Desktop\_Thesis\Test_images'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "/sensor/dlsu/node-1/images":
        print(msg.topic)
        print(msg.payload)
        payload = json.loads(msg.payload)
        filename = payload['filename']
        print("hello world!")
        # splitFilename = filename.split('_')
        # dateStr = splitFilename[1]
        # with open(dest + '/' + dateStr + '/' + filename, 'wb') as f:
        #     f.write(binascii.a2b_base64(payload['image_data']))
        #     print("image successfully received")


def on_publish(client, userdata, mid):
    print("Message published")

client = mqtt.Client("Server")
client.connect(mqttIP, mqttPort)

client.loop_start()

client.subscribe("/sensor/dlsu/node-1/images")
client.on_connect = on_connect
time.sleep(30)
client.on_message = on_message
client.loop_end()


# client.on_publish = on_publish
# #client.subscribe("/sensor/dlsu/node-1/images")

# client.loop_forever()
