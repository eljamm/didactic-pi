# WORK IN PROGRESS

import json
import logging
from time import sleep

from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory


class Ultrasound:
    def __init__(self, pins, pin_factory=PiGPIOFactory(),
                 setup=False):
        self.echo = pins["E"]
        self.trigger = pins["T"]
        self.pin_factory = pin_factory

        if setup:
            self.setup()

    def setup(self):
        self.device = DistanceSensor(
            echo=self.echo, trigger=self.trigger, pin_factory=self.pin_factory)

    def read(self):
        data = sensor.distance*100

        json_file = {
            "sensor": "ultrasonic",
            "message": data,
            "message_type": "data",
        }

        return json_file

    def process(self, ws, delay):
        try:
            json_file = self.read()

            # Send data if json_file is not empty
            if not len(json_file) == 0:
                ws.send(json.dumps(json_file))

            sleep(delay)

        except (RuntimeError, TypeError) as error:
            logging.warning(error.args[0])
            sleep(2.0)


if __name__ == "__main__":
    pins = {
        "T": 18,
        "E": 17
    }

    sensor = Ultrasound(pins)

    sensor.wait_for_active()

    while True:
        print('Distance: ', sensor.distance * 100)
        sleep(1)
