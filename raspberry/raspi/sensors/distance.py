import json
import logging
from time import sleep

from gpiozero import DistanceSensor


class Ultrasonic:
    def __init__(self, pins, setup=False):
        self.echo = pins["E"]
        self.trigger = pins["T"]

        if setup:
            self.setup()

    def setup(self):
        self.device = DistanceSensor(echo=self.echo, trigger=self.trigger)

    def cleanup(self):
        self.device.close()

    def read(self):
        distance = self.device.distance*100

        message = "Distance: {:.1f} cm".format(distance)

        json_file = {
            "sensor": "ultrasonic",
            "message": message,
            "message_type": "data",
            "distance": distance
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

    sensor = Ultrasonic(pins, setup=True)

    try:
        while True:
            distance = sensor.device.distance*100
            print('Distance: ', "Distance: {:.1f} cm".format(distance))
            sleep(1)
    except KeyboardInterrupt:
        sensor.cleanup()
        print("\nQuitting Program")
