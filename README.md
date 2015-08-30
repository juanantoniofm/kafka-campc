
The Kafka Conspiracy


## Setup

Modify the `settings.py` file with your environmental settings.

make sure the `$DISPLAY` variable is correctly setup to your display number


## Usage

run the grabber as daemon

	python camgrab.py | tee -a camgrab.$(date +%F).log &

run the uploader as a one-shot

	python camup.py



## Know errors

### `Gtk-WARNING **: cannot open display:`

Make sure the `$DISPLAY` var is setup with

	export DISPLAY=:0

that will work in most cases.


