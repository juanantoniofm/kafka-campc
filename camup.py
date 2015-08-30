#!/usr/bin/python

"""
The part of the tool that does the publishing to kafka.

It gets images from the directory, locks them, creates the message and moves the files
"""

import settings
import os


def read_dir(path = None):
    try:
        listing = os.listdir(path)
        print listing 
        return listing
    except OSError as e:
        # ALways the doubt.. should I raise here or up?
        print e
        return None


def get_first_picture(filelist):
    """
    process a list of files and finds the first picture
    """
    if filelist is None: return None 
    extensions = ["jpeg",".jpg",".png","tiff",".raw",".bmp"] # Fiesta!!!
    for file in filelist:
        if file[-4:].lower() in extensions:
            return file

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def clean_files(filelist=None):
    """clean the environment"""
    assert type(filelist) == type([])
    for fileitem in filelist:
        os.remove(fileitem)

def publish(topic, message):
    """just a mock
    """
    print("INFO:","publishing to topic {0}:".format(topic))
    yesorno = raw_input("Submitt a message?: ")
    if yesorno == "yes":
        print "INFO:","Succesfully submitted"
        return "ok"
    else:
        print yesorno
        print "INFO:","Not submitted by command of the lord"
        return  None


if __name__=="__main__":
    print("INFO:","Working dir {0}".format(settings.SAVE_FOLDER))
    picture_name = get_first_picture(read_dir(settings.SAVE_FOLDER))
    # the picture file wont be created if there are no pictures. 
    # then we should wait and try again later
    picture_file = os.path.join(settings.SAVE_FOLDER,picture_name)
    print "this is the first picture", picture_file
    lockfile=picture_file + ".lock"
    touch(lockfile)
    print("DEBUG:","picture locked")
    print "DEBUG","Creating the message"

    if publish("campics","picturemessage"):
        clean_files([picture_file,lockfile])

