#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import json
import random

import markdown

from flask import Flask, Markup, request, send_file
app = Flask(__name__)

from camup import acquire_a_picture, build_message, publish, clean_files

from settings import SAVE_FOLDER, TOPIC, KAFKA_SERVER


@app.route('/', methods=["GET"])
def main_menu():
    return """
    This is the API main page.
    we are connecting to the server {0}
    on the topic {1}, 
    taking pictures from {2}
    """.format(
            KAFKA_SERVER,
            TOPIC,
            SAVE_FOLDER
            )

@app.route("/image/<picture>", methods=["GET"])
def get_image(picture = None):

    
    img, img_id = acquire_a_picture(lockit=False, last=True)
    picture_file = os.path.join(SAVE_FOLDER, "{0}.jpg".format(img_id) )
    return send_file(picture_file)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, debug=True)

