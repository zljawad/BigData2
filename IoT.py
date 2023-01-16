#!/usr/bin/env python3
import paho.mqtt.client as mqtt

import json
from kafka import KafkaProducer
from pymongo import MongoClient
from datetime import datetime
import math
from kafka import KafkaProducer
data=""
def serializer(message):
        return json.dumps(message).encode('utf-8')
  
#Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)
    
def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("device/temphum")
def on_message(client, userdata, msg):
    data = f"{msg.payload}"
    temp = data[2:7]
    hum = data[14:19]
    dic = {"date" : str(datetime.now()), "temp" : temp , "hum" : hum}
    print(dic)
    producer.send('test', dic)
    #kafka_producer(temp[0:5],hum[0:5])
client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set("myusername", "aeNg8aibai0oiloo7xiad1iaju1uch")
client.connect('91.121.93.94', 1883)
client.loop_forever()  # Start networking daemon



