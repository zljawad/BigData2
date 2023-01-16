import csv 
import requests
import json
from kafka import KafkaProducer
from pymongo import MongoClient
from datetime import datetime
import math
from kafka import KafkaProducer
if __name__ == "__main__":
    client = MongoClient()

    # Récupération des données météorologique 
    response_API = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=30.427755&lon=-9.598107&appid=1d24a7642028701ea76d7f6b86ee4705")
    data = response_API.text
    parse_json = json.loads(data)
    temp = parse_json['main']['temp']
    hum = parse_json['main']['humidity']
    temp = round(float(temp) - 273.15,2)


    dic = {"date" : str(datetime.now()), "temp" : temp , "hum" : hum}

    # serialisation de message en JSON
    def serializer(message):
        return json.dumps(message).encode('utf-8')

    # Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )

    producer.send('test', dic)

    # La création et stockage des données dans MongoDB
    mydb = client["weather"]
    mycol = mydb["data"]
    mydict = { "Temp": temp, "Humidity": hum }
    x = mycol.insert_one(mydict)


        