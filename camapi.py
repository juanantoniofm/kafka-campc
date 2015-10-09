#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
# Cam API

The main way of controlling the machine is 
through a web interface. 

Currently, is a hacky solution, splitted in different components.

### camup.py

holds methods to upload pictures to kafka


### cam_*

are files with workers for the threaded communicacion with Kafka

### camgrab.py

takes care of grabbing pictures from the camera

and so on... ;) 

happy hacking 
"""

import os

import json # for obvious reasons
import random # soon will be not needed
 
import base64 # used to encode the pictures
import threading # used to create threads for consumers and producers
import logging, time # for sanity and quality, proper logging

from kafka.client import KafkaClient # simple implementations to make our lives easy
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

import markdown # to process markdown into nice HTML for the automated documentation

from flask import Flask, Markup, request, send_file, render_template
app = Flask(__name__)

from camup import acquire_a_picture, build_message, publish, clean_files

from settings import SAVE_FOLDER, TOPIC, KAFKA_SERVER


@app.route('/help', methods=["GET"])
def documentation():
    return "Yo,dawg"
    #return Markup(markdown.markdown(__doc__))


@app.route('/', methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/local/image/last", methods=["GET"])
def get_image(picture = None):
    """
    plain and simple, get the last picture and send it to the client
    """
    try:
        img, img_id = acquire_a_picture(lockit=False, last=True)
    except AssertionError:
        return render_template("error.html"), 404

    picture_file = os.path.join(SAVE_FOLDER, "{0}.jpg".format(img_id) )
    return send_file(picture_file)

@app.route("/remote/image/last", methods=["GET"])
def trigger_threads():
    """
    start the threads - test
    """
    import cammain
    #heartbeat = cammain.Heartbeat()
    consumer = cammain.Consumer()
    consumer.start() # TODO: this level of abstraction is borkd
    return "deberia tener una imagen en jpeg para escupir"
    
    return "todo"


# TODO:
# we have to make it spin up the threads to communicate with kafka
# then add health checks to that
# then we wil have a local health check and kafka real heartbeat


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.DEBUG
        )

    app.run(host="0.0.0.0", port=8088, debug=True)

