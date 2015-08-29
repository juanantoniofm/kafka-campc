#!/usr/bin/python

TIME_WINDOW=15 # seconds to keep the window open
PICTURE_INTERVAL=25 # take a picture every this seconds



# example taken from stackoverflow
# http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# Using OpenCV
################################################################################
#   WARNING: this is a hack, not prod ready in any way.
################################################################################

# Better than OpenCV, for a professional scenario with cannon cameras, for example, we would need to use
# something like libgphoto2.


from time import sleep
from cv2 import *



def grab_pic(camera_index=0):
    """
    take a picture from the specified camera
    camera_index :: default = 0; just the number of the cam on the system (is compatible with many)
    """
    try:
        cam = VideoCapture(camera_index)
        s, img = cam.read()
        if s: # the frame was captured without errors
            return img
        else:
            raise IOError("Sorry, couldn't get the picture")
    except IOError as e:
        print("ERROR",e)
        return None
    #return img # TODO:Confirm that img is None upon failure to be able to enable this code



def display_picture(picture = None):
    """
    just create a simple window to display the picture. 
    The window should go away after a few seconds
    TODO: for now I have implemented the keypress to close the window
    """
    assert picture is not None # as it means that no pic has been passed
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    imshow("cam-test",picture)
    waitKey(TIME_WINDOW)
    destroyWindow("cam-test")


def save_picture(picture=None):
    """
    save the picture to disk
    """
    imwrite("filename.jpg",picture) #save image
    print("INFO","Picture saved")


if __name__=="__main__":
    """
    """
    # we start grabbing pictures every 10 seconds or so

    while True:
        print("INFO","Taking pictures and stuff")
        camera = 0 # the index for the camera. It should be taken from settings, or a default which is 0 often
        picture = grab_pic(camera) # get the actual picture from the camera
        display_picture(picture) # open a window with it
        save_picture(picture) # put it in a file
        sleep(PICTURE_INTERVAL)
