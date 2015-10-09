#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import time
import threading

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

import settings

class Heartbeat(threading.Thread):
    daemon = True

    def run(self):
        self.client = KafkaClient(settings.KAFKA_SERVER)
        self.producer = SimpleProducer(self.client)

        while True:
            self.producer.send_messages('heartbeats', """{"id":str(uuid.uuid4()), "status": 200, "serviceName":"chewit_cam" }""")
            time.sleep(5)

