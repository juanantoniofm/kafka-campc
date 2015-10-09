#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading

import settings
from camgrab import grab_pic

class Grabber(threading.Thread):
    daemon = True

    def run(self):
        while True:
            print "getting pic"
            
            time.sleep(settings.PICTURE_INTERVAL)

    
