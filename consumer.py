from kafka import KafkaConsumer
from datetime import datetime
import time
import pickle

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

a_file = open("dictionary_scraping/dictionary_activities.pkl", "wb")
pickle.dump(diz, a_file)
a_file.close()