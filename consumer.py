from kafka import KafkaConsumer
import pymongo
from pymongo import MongoClient

consumer = KafkaConsumer(
    'INSERT TOPIC NAME',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

diz={}
for message in consumer:
    message = message.value
    diz.update(message)

client = MongoClient('localhost:27017')

#Database 
db = client["Strava"]

#Collection
collection = db["INSERT TOPIC NAME"]

for el in diz:
    j = prova[el]
    j["ID"] = el
    #Insert each document in the collection
    collection.insert_one(j)
