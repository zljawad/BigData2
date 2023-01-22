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
    api = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=30.427755&lon=-9.598107&appid=id"
    #response_API = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=30.427755&lon=-9.598107&appid=id")
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(data)
    count = len(parse_json['list'])
    print(count)
    temp = []
    hum = []
    date = []
    for i in range(0,count):
        tem = parse_json['list'][i]['main']['temp']
        hu = parse_json['list'][i]['main']['humidity']
        dt = parse_json['list'][i]['dt_txt']
        dt = dt[0:16]
        tem = round(float(tem) - 273.15,2)
        temp.append(tem)
        hum.append(hu)
        date.append(dt)

    dic2 = {"date" : date, "temp" : temp , "hum" : hum}

    # serialisation de message en JSON
    def serializer(message):
        return json.dumps(message).encode('utf-8')

    # Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )

    producer.send('embarquee', dic2)     
