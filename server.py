import asyncio
import websockets
import csv 
import requests
import json
from kafka import KafkaProducer
from pymongo import MongoClient
from datetime import datetime
import math
from kafka import KafkaProducer

async def echo(websocket):
    #async for message in websocket:
    api = "https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=30.427755&lon=-9.598107&appid=id"
    response_API = requests.get(api)
    data = response_API.text
    parse_json = json.loads(data)
    count = len(parse_json['list'])
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
    await websocket.send(json.dumps(dic2))

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
