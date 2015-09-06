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

from kafka import SimpleProducer, KafkaClient  # pragma: no cover
from kafka.common import *  # pragma: no cover

def read_dir(path = None):
    assert path is not None
    try:
        listing = os.listdir(path)
        print "DEBUG:", listing 
        return listing
    except OSError as e:
        # ALways the doubt.. should I raise here or up?
        print("ERROR", e)
        raise 
        

def is_locked(file):
    """
    find out if a picture is being processed by some other thread
    """
    return True



def get_first_picture(filelist):
    """ 
    process a list of files and finds the first picture.
    if the picture is locked, get the next one.
    """
    if filelist is None: 
        raise ValueError("No file list provided or wrong working folder")
    extensions = ["jpeg",".jpg",".png","tiff",".raw",".bmp"] # Fiesta!!!
    for file in filelist:
        if file[-4:].lower() in extensions:
            if is_locked(file):
                continue
            else:
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
    yesorno = raw_input("Submitt a message?: ")
    if "y" in yesorno[0:1]:
        send_message(msg)
        print "INFO:","Succesfully submitted"
        return "ok"
    else:
        print yesorno
        print "INFO:","Not submitted by command of the lord"
        return  None


def build_message(img_id,img):
    """
    builds a message for kafka in json with the picture encoded in base64
    and returns the byte stream
    """
    json_data = {
            "image_id":img_id,
            "image": base64.encodestring(img)
            }
    # convert to json
    json_string = json.dumps(json_data)
    # convert to binary 
    msg = "".join(format(x, "b") for x in bytearray(json_string))
    return msg


def send_message(msg):
    """
    to kafka with love
    """

    # Verify we got a legit message
    assert type(msg) is type(b"foo")
    # To send messages synchronously
    kafka = KafkaClient(settings.KAFKA_SERVER)
    print "INFO:","client clienting"
    producer = SimpleProducer(kafka)
    print "INFO:","producer producing"

    while True:
        try:
            # Note that the application is responsible for
            # encoding messages to bytes type
            producer.send_messages(b'{0}'.format(settings.TOPIC), msg)
            return "Ok"
        except (InvalidMessageError,
                InvalidFetchRequestError,
                MessageSizeTooLargeError) as e:
            print "WARNING:", "Your message is fucky or Kafka is not properly configured;",   e.message
            sleep(2)
            continue

        except Exception as e:
            #TODO: Pokemon exception. Please enable traceback logging
            print "ERROR:", "adunno. Kafka seem f'd up", e
            continue


    # Send unicode message
    #producer.send_messages(b'one-topic01', u'你怎么样?'.encode('utf-8'))
    return "Ok"


def lock_picture(img_filename):
    """
    set a lock in filesystem, and maybe other queues/semaphores/monitors
    """
    lockfile=img_filename + ".lock"
    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    touch(lockfile)
    print("DEBUG:","picture locked")
    return lockfile


def acquire_a_picture():  # pragma: no cover
    picture_name = get_first_picture(read_dir(settings.SAVE_FOLDER))
    assert picture_name is not None
    # the picture file wont be found if there are no pictures. 
    # then we should wait and try again later
    # but we plan to do it at a higher stage (ie the caller)
    picture_file = os.path.join(settings.SAVE_FOLDER,picture_name)
    img_id = picture_name.split(".")[0]
    print "DEBUG:", "this is the first picture", img_id
    lock_picture(picture_name)
    with open(picture_file) as img_file:
        img = img_file.read()
    return img, img_id


if __name__=="__main__":  # pragma: no cover
    # Printing initial information
    print "INFO:", dir(settings)
    print "INFO:", "SAVE FOLDER:", settings.SAVE_FOLDER
    print("INFO:","Working dir {0};".format(settings.SAVE_FOLDER))

    img, img_id = acquire_a_picture()

    print "DEBUG","Creating the message"
    msg =  build_message(img_id, img)

    if publish(settings.TOPIC, msg):
        clean_files([picture_file,lockfile])




