#!/usr/bin/python
# -*- coding: utf-8 -*-


"""  # pragma: no cover
The part of the tool that does the publishing to kafka.

It gets images from the directory, locks them, creates the message and moves the files
"""

import settings  # pragma: no cover
import os  # pragma: no cover
from time import sleep  # pragma: no cover

import base64  # pragma: no cover
import json  # pragma: no cover
import uuid # pragma: no cover

from kafka import SimpleProducer, KafkaClient  # pragma: no cover
from kafka.common import *  # pragma: no cover

def read_dir(path = None):
    assert path is not None
    try:
        listing = os.listdir(path)
        print( "DEBUG:", listing )
        return listing
    except OSError as e:
        # ALways the doubt.. should I raise here or up?
        print("ERROR", e)
        raise 
        

def is_locked(file=None, filelist=None, path = None):
    """
    find out if a picture is being processed by some other thread.
    TODO: decice if we can overcome the listing in the params instead of None
    """
    assert file is not None
    if filelist is None:
        # then try to read the path
        if path is not None:
            filelist = read_dir(path)
        else:
            raise ValueError("WTF m8. Give me a directory or a filelist")
    if file+".lock" in filelist:
        return True
    else:
        return False



def get_picture_from_storage(filelist = None, reverse = False):
    """ 
    process a list of files and finds the first picture.
    if the picture is locked, get the next one.
    """
    if filelist is None: 
        raise ValueError("No file list provided or wrong working folder")
    extensions = ["jpeg",".jpg",".png","tiff",".raw",".bmp"] # Fiesta!!!
    filelist.sort(reverse=reverse)
    for file in filelist:
        if file[-4:].lower() in extensions:
            if is_locked(file, filelist):
                print("DEBUG:",file,"is locked. Get next")
                continue
            else:
                print("DEBUG:",file,"acquired. giving that")
                return file


def clean_files(filelist=None):
    """clean the environment"""
    assert type(filelist) == type([])
    for fileitem in filelist:
        os.remove(fileitem)

def publish(topic, msg):
    """
    just a wrapper on send_message to be able to control if sending or not in this preview. 
    topic :: Is not really needed, but i put it for wrapping and logging purposes
    """
    print("INFO:","publishing to topic {0}:".format(topic))
    result = send_message(msg)
    if result > 200:
        print "ERROR:" ,"sender returned {0}".format(result)
    elif result == 200:
        print( "INFO:","Succesfully submitted")
    return result


def confirmation_publish(topic, msg):
    """
    just a wrapper on send_message to be able to control if sending or not in this preview. 
    topic :: Is not really needed, but i put it for wrapping and logging purposes
    """
    print("INFO:","publishing to topic {0}:".format(topic))
    #yesorno = raw_input("Submitt a message?: ") # TODO: configure this
    yesorno = "yes" # upload by defo
    if "y" in yesorno[0:1]:
        send_message(msg)
        print( "INFO:","Succesfully submitted")
        return "ok"
    else:
        print( "INFO:","Not submitted by command of the lord")
        return  None


def build_message(img_id,img,barcode = None):
    """
    builds a message for kafka in json with the picture encoded in base64
    and returns the byte stream
    """
    assert len(img_id) < 1000 # to avoid confusing bin and id
    json_data = {
            "id":str(uuid.uuid4()),
            "pictureName":img_id,
            "image": base64.encodestring(img),
            "barcode": "bull-seat" if not barcode else barcode,
            "ride": "chewit"
            }
    # convert to json
    json_string = json.dumps(json_data)
    # convert to binary 
    return json_string


def send_message(msg, retries = 5):
    """
    to kafka with love
    """

    # Verify we got a legit message
    assert type(msg) is type(b"foo")
    # To send messages synchronously
    kafka = KafkaClient(settings.KAFKA_SERVER)
    print( "INFO:","client clienting")
    producer = SimpleProducer(kafka)
    print( "INFO:","producer producing")

    while retries >= 0:
        retries -= 1
        try:
            # Note that the application is responsible for
            # encoding messages to bytes type
            producer.send_messages(b'{0}'.format(settings.TOPIC), msg)
            return 200 # Ok
        except (InvalidMessageError,
                InvalidFetchRequestError,
                MessageSizeTooLargeError) as e:
            print( "WARNING:", "Your message is fucky or Kafka is not properly configured;",   e.message)
            sleep(2)
            continue

        except Exception as e:
            #TODO: Pokemon exception. Please enable traceback logging
            print( "ERROR:", "adunno. Kafka seem f'd up", e)
            continue


    # Send unicode message
    #producer.send_messages(b'one-topic01', u'你怎么样?'.encode('utf-8'))
    return 500 #If we arrived here, we have a problem


def lock_picture(img_filename):
    """
    set a lock in filesystem, and maybe other queues/semaphores/monitors
    """
    lockfile=os.path.join(settings.SAVE_FOLDER,img_filename + ".lock")
    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    touch(lockfile)
    print("DEBUG:","picture locked")
    return lockfile


def acquire_a_picture(lockit = True, last = False):  
    picture_name = get_picture_from_storage(read_dir(settings.SAVE_FOLDER), last)
    assert picture_name is not None
    # the picture file wont be found if there are no pictures. 
    # then we should wait and try again later
    # but we plan to do it at a higher stage (ie the caller)
    picture_file = os.path.join(settings.SAVE_FOLDER,picture_name)
    img_id = picture_name.split(".")[0]
    print( "DEBUG:", "this is the first picture", img_id)
    if lockit:
        lock_picture(picture_name)
    with open(picture_file) as img_file:
        img = img_file.read()
    return img, img_id


def upload_next():
    """
    just upload the next picture
    """

    try:
        img, img_id = acquire_a_picture()
    except AssertionError:
        print "No more pictures to process"
        return 404

    print( "DEBUG","Creating the message")
    msg =  build_message(img_id, img)

    publishing = publish(settings.TOPIC, msg)
    if publishing == 200:
        # If we can publish successfully, clean up
        picture_file = settings.SAVE_FOLDER + "/" + img_id + ".jpg"
        lockfile = picture_file + ".lock"
        clean_files([picture_file,lockfile])
    if publishing == 500:
        # something went wrong, we might have to do carefull clean up
        picture_file = settings.SAVE_FOLDER + "/" + img_id + ".jpg"
        lockfile = picture_file + ".lock"
        clean_files([lockfile])


    return 200 #TODO: maybe we can use this to complete the heartbeat?


if __name__=="__main__":  # pragma: no cover
    # Printing initial information
    print( "INFO:", dir(settings))
    print( "INFO:", "SAVE FOLDER:", settings.SAVE_FOLDER)
    print("INFO:","Working dir {0};".format(settings.SAVE_FOLDER))

    upload_next()

