import argparse
import threading
import time
from typing import Any, Dict

import numpy as np
import paho.mqtt.client as mqtt

AVERAGE_SEC_PER_ARRIVAL = 5


def publisher_thread_task(client: mqtt.Client, client_lock: threading.Lock, msg: str):
    while True:
        client_lock.acquire()
        client.publish("iot-lab-ss21-group4/count-event", msg)
        client_lock.release()
        print("published: {}".format(msg))
        interarrival_time = np.random.exponential(scale=AVERAGE_SEC_PER_ARRIVAL)
        time.sleep(interarrival_time)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client: mqtt.Client, userdata: Dict[str, Any], flags: Dict[str, int], rc: int):
    print("Connected with result code " + str(rc))
    client_lock: threading.Lock = userdata["client_lock"]
    if not userdata["is_connected"]:
        client_lock.release()
        userdata["is_connected"] = True


def on_disconnect(client: mqtt.Client, userdata: Dict[str, Any], rc: int):
    print("Disconnected with result code " + str(rc))
    client_lock: threading.Lock = userdata["client_lock"]
    if userdata["is_connected"]:
        client_lock.acquire()
        userdata["is_connected"] = False


def main(args: argparse.Namespace):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client_lock = threading.Lock()
    client_lock.acquire()

    enter_publisher = threading.Thread(target=publisher_thread_task, args=(client, client_lock, "entered"))
    enter_publisher.start()
    exit_publisher = threading.Thread(target=publisher_thread_task, args=(client, client_lock, "exited"))
    exit_publisher.start()
    user_data = {
        "client_lock": client_lock,
        "is_connected": False,
    }
    client.user_data_set(user_data)
    client.connect(args.broker_uri, port=1883)
    client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker-uri", type=str, default="test.mosquitto.org", help="URI of the MQTT broker to publish data.")
    main(parser.parse_args())
