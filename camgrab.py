#!/usr/bin/python

import settings 

#TIME_WINDOW=settings.TIME_WINDOW if settings.TIME_WINDOW is not None else 15 # seconds to keep the window open
TIME_WINDOW=1
#PICTURE_INTERVAL=settings.PICTURE_INTERVAL or 25 # take a image every this seconds
PICTURE_INTERVAL=2
CAMERA=settings.CAMERA or 0 # the id of the camera for openCV (maybe /dev/video<number> )
SAVE_FOLDER=settings.SAVE_FOLDER or "." # folder to put pictures and barcodes

limit=20 # limit the number of pictures to take in case something goes wonky


# example taken from stackoverflow
# http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# Using OpenCV
################################################################################
#   WARNING: this is a hack, not prod ready in any way.
################################################################################

# Better than OpenCV, for a professional scenario with cannon cameras, for example, we would need to use
# something like libgphoto2.


import time

from genutils import *


def grab_pic(camera_index=0):
    """
    take a image from the specified camera
    camera_index :: default = 0; just the number of the cam on the system (is compatible with many)
    """
    cam = VideoCapture(camera_index)
    s, img = cam.read()
    if s: # the frame was captured without errors
        msg =  "DEBUG: Picture retrieved without errors"
        print "INFO:", msg
        return img, msg
    else:
        msg = "ERROR: Couldn't retrieve image from camera {0}".format(camera_index)
        print("INFO:", msg)
        return None, msg

    #return img # TODO:Confirm that image is None upon failure to be able to enable this code


def get_img_id(timestamp=None, camera=None):
    """
    create an id for the image. Uses timestamp and camera of origin.
    timestamp :: seconds since epoch (in UTC usually)
    camera :: a string to identify the camera of origin
    """
    assert camera is not None
    assert timestamp is not None
    timeString = time.strftime("%Y%m%d_%H%M_%S", timestamp)
    return "{0}_cam{1}".format(timeString,camera)


if __name__=="__main__":
    """
    """
    # we start grabbing image every 10 seconds or so

    for x in range(limit):
        print("INFO","Taking image and stuff")
        img,msg = grab_pic(CAMERA) # get the actual image from the camera
        img_id = get_img_id(time.gmtime(), CAMERA)  # get an id to track the picture
        display_image(img, img_id) # open a window with it
        save_image(img, img_id) # put it in a file
        time.sleep(PICTURE_INTERVAL)
