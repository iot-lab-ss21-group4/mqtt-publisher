# MQTT publisher
It uses `paho-mqtt` to send "entered" and "exited" messages to `iot-lab-ss21-group4/count-event` topic at some public MQTT broker.

## **Installing Dependencies:**
* Install Python3 either system-wide, user-wide or as a virtual environment,
* Run `pip install pip-tools` command via the `pip` command associated with the installed Python,
* Run `pip-sync` inside the project root folder.

## **Usage:**
    usage: main.py [-h] [--broker-uri BROKER_URI]

    optional arguments:
    -h, --help            show this help message and exit
    --broker-uri BROKER_URI
                            URI of the MQTT broker to publish data.
