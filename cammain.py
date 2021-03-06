#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

# The cam main

a caiman

"""

import base64
import threading, logging, time
import uuid

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

import settings
from genutils import process_message_from_kafka
import camapi
import camup

from cam_heartbeat import Heartbeat
#from cam_picupload import PicUpload # not in use, we go for functions
from cam_grab import Grabber # the one that takes the pictures

################################################################################
import threading
import atexit

POOL_TIME = 5 #Seconds

# variables that are accessible from anywhere
commonDataStruct = {}
# lock to control access to variable
dataLock = threading.Lock()
# thread handler
heartThread = Heartbeat()
grabThread = Grabber()
consumerThread = threading.Thread()


def create_app():
    app = camapi.app

    def interrupt():
        global uploadThread
        global heartThread
        global grabThread
        uploadThread.cancel() # only the Timer has cancel

    def upload_now():
        global commonDataStruct
        global uploadThread
        print "uploading"
        with dataLock:
            print "Uploading locked"
            camup.upload_next()
            
        uploadThread = threading.Timer(POOL_TIME, upload_now, ())
        uploadThread.start()


    def upload_start():
        """
        Start the upload worker.
        Instead of using an object, relies in functions
        """
        global uploadThread
        print("Starting upload")
        uploadThread = threading.Timer(POOL_TIME, upload_now , ())
        uploadThread.start()


    def consume_now():
        """
        consume a pic from kafka
        """
        client = KafkaClient(settings.KAFKA_SERVER)
        consumer = SimpleConsumer(client, "my_group", "pictures", fetch_size_bytes=30000000)
        for message in consumer:
            print message
            #TODO: to write



    def monitor_start():
        """
        go and get pics from kafka
        """
        print("getting pics from Kafka")
        consumerThread = threading.Timer(POOL_TIME, consume_now, ())
        consumerThread.start()
        
    # Initiate
    threads = [
            heartThread,
            grabThread
            ]
    for t in threads:
        print "starting Thread {0}".format(type(t))
        t.start()


    upload_start()

    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app

print "starting"
app = create_app()  

#app.run(host="0.0.0.0", port=8088, debug=True)
