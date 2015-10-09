#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
import uuid

import settings
from camgrab import grab_pic
from genutils import save_image

class Grabber(threading.Thread):
    daemon = True

    def run(self):
        while True:
            img, msg = grab_pic(settings.CAMERA)
            img_id = uuid.uuid4()
            save_image(img, img_id) # put it in a file
            print "taken pic"
            
            time.sleep(settings.PICTURE_INTERVAL)

    