
"""
small library with common methods for the campc.

The name of this library is a little joke to our C devs

"""

from cv2 import *
import settings


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
    print "DEBUG:", "TIME_WINDOWN type: ", type(settings.TIME_WINDOW)
        # TODO: for some extrange reason, using an int variable doesnt work. 
        # python passes by object reference (object references are passed by value)
        # so it should work.
    waitKey(300) # so this should be TIME_WINDOW not an int
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
        imwrite(r"{0}/{1}.jpg".format(settings.SAVE_FOLDER,img_id)
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


