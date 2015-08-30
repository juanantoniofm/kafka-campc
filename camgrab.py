#!/usr/bin/python

import settings 

print dir(settings)
#TIME_WINDOW=settings.TIME_WINDOW if settings.TIME_WINDOW is not None else 15 # seconds to keep the window open
TIME_WINDOW=15
#PICTURE_INTERVAL=settings.PICTURE_INTERVAL or 25 # take a image every this seconds
PICTURE_INTERVAL=25
CAMERA=settings.CAMERA or 0 # the id of the camera for openCV (maybe /dev/video<number> )
SAVE_FOLDER=settings.SAVE_FOLDER or "." # folder to put pictures and barcodes



# example taken from stackoverflow
# http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# Using OpenCV
################################################################################
#   WARNING: this is a hack, not prod ready in any way.
################################################################################

# Better than OpenCV, for a professional scenario with cannon cameras, for example, we would need to use
# something like libgphoto2.


import time
from cv2 import *



def grab_pic(camera_index=0):
    """
    take a image from the specified camera
    camera_index :: default = 0; just the number of the cam on the system (is compatible with many)
    """
    cam = VideoCapture(camera_index)
    s, img = cam.read()
    if s: # the frame was captured without errors
        msg =  "DEBUG: Picture retrieved without errors"
        print msg
        return img, msg
    else:
        msg = "ERROR: Couldn't retrieve image from camera {0}".format(camera_index)
        print(msg)
        return None, msg

    #return img # TODO:Confirm that image is None upon failure to be able to enable this code



def display_image(img = None,img_id=None):
    """
    just create a simple window to display the image. 
    The window should go away after a few seconds
    TODO: for now I have implemented the keypress to close the window
    """
    assert img is not None # as it means that no pic has been passed
    assert img_id is not None # as it means that no pic has been passed
    windowName = "{0}".format(img_id)
    namedWindow(windowName,CV_WINDOW_AUTOSIZE)
    imshow(windowName,img)
    print "DEBUG:", "TIME_WINDOWN type: ", type(TIME_WINDOW)
        # TODO: for some extrange reason, using an int variable doesnt work. 
        # python passes by object reference (object references are passed by value)
        # so it should work.
    waitKey(300)
    destroyWindow("cam-test")
    return img, "INFO: image {0} displayed".format(img_id)


def save_image(img=None,img_id=None):
    """
    save the image to disk
    img :: the picture blob
    img_id :: a pregenerated id for this image
    """
    assert img is not None
    assert img_id is not None
    try:
        imwrite(r"{0}/{1}.jpg".format(SAVE_FOLDER,img_id)
                ,img
                ,[IMWRITE_JPEG_QUALITY,100]) #save image
        print("INFO","Picture {0} saved".format(img_id))
        msg = "INFO \t saved image {0}".format(img_id)
    except Exception as e:
        #TODO: Pokemon exception. Please remove
        msg = "ERROR \t Unable to save image {0},{1}".format(
            img_id,
            e)
        print("ERROR", msg)
    return img,msg 


def get_img_id(timestamp, camera):
    """
    create an id for the image. Uses timestamp and camera of origin.
    timestamp :: seconds since epoch (in UTC usually)
    camera :: a string to identify the camera of origin
    """
    timeString = time.strftime("%Y%m%d_%H%M_%S", timestamp)
    return "{0}_cam{1}".format(timeString,camera)


if __name__=="__main__":
    """
    """
    # we start grabbing image every 10 seconds or so

    for x in range(2):
        print("INFO","Taking image and stuff")
        img,msg = grab_pic(CAMERA) # get the actual image from the camera
        img_id = get_img_id(time.gmtime(), CAMERA)  # get an id to track the picture
        display_image(img, img_id) # open a window with it
        save_image(img, img_id) # put it in a file
        time.sleep(PICTURE_INTERVAL)
