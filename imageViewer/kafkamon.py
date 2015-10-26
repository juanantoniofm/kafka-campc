#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import threading, logging, time

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

import settings

class Heartbeat(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient(settings.KAFKA_SERVER)
        producer = SimpleProducer(client)

        while True:
            producer.send_messages('heartbeats', """{"id":"yes-is-a-fake-uuide", "status": 200, "serviceName":"chewit_cam" }""")
            time.sleep(5)


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient("localhost:9092")
        consumer = SimpleConsumer(client, "my_group", "pictures", fetch_size_bytes=30000000)

        for message in consumer:
            print message 
            img_bin = message["image"]
            img_id = message["id"]
            barcode = message["barcode"] if message["barcode"] else None
            ride = message["ride"]

            with open("last_pic.jpeg", "w") as fh:
                img_data = base64.decodestring(img_bin)
                fh.write(img_data)
                print "image written"
 
            

def main():
    threads = [
        Heartbeat(),
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.DEBUG
        )
    main()
