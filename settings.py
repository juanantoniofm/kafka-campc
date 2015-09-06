
"""
This is the settings file.
Here you should have the bare minimum needed to run the software, 
but if you miss a setting it will just use the default.

The commented out settings are here just for reference.

TODO: either delete or use proper explanations
TODO: this is the most naive way of doing "settings". rely on zookeper? :)
"""

TIME_WINDOW=15 # seconds to keep the window open
#PICTURE_INTERVAL=25 # take a image every this seconds
CAMERA=0 # the id of the camera for openCV (maybe /dev/video<number> )
SAVE_FOLDER="captures" # folder to put pictures and barcodes. default to current dir.
TOPIC="cameras"

KAFKA_SERVER="localhost:9092"
