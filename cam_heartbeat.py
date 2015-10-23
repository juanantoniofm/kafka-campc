#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import time
import threading
import json

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

import settings

class Heartbeat(threading.Thread):
    #daemon = True

    def run(self):
        self.client = KafkaClient(settings.KAFKA_SERVER)
        self.producer = SimpleProducer(self.client)

        while True:
            data = {
                    "id": str(uuid.uuid4()),
                    "status":200,
                    "serviceName": settings.RIDE
                    }
            self.producer.send_messages("heartbeats", json.dumps(data))
            time.sleep(5)

