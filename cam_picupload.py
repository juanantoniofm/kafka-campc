

"""
this might not be needed at all
"""
import threading, logging, time

import uuid

from kafhka.client import KafkaClient
from kafka.producer import SimpleProducer

import settings
from genutils import process_message_from_kafka
from cam_hearbeat import HeartBeat


class PicUpload(threading.Thread):
    daemon = True
    def run(self):
        print "uploadingggggggggggggg"
        import camup
        while True:
            result = camup.upload_next()
            print "upload: {0}".format(result)

