import json
import logging
import textwrap
from time import sleep

import adafruit_dht
import board
import coloredlogs


class DHT11:
    def __init__(self, pin, logger):
        self.device = adafruit_dht.DHT11(pin, use_pulseio=False)
        self.logger = logger

    def readDHT(self):
        try:
            temp = self.device.temperature
            temp_f = temp * (9 / 5) + 32
            hum = self.device.humidity

            message = "Temp: {:.1f} F / {:.1f} C    Humidity: {}%".format(
                temp_f, temp, hum)

            json_file = {
                "sensor": "dht11",
                "message": message,
                "message_type": "data",
                "temp": temp,
                "hum": hum
            }

            return json_file

        except (RuntimeError, TypeError) as error:
            self.logger.warning(error.args[0])
            sleep(2.0)
            return {}

    def processDHT(self, ws, delay):
        try:
            json_file = self.readDHT()

            # Send data if json_file is not empty
            if not len(json_file) == 0:
                ws.send(json.dumps(json_file))

            sleep(delay)

        except (RuntimeError, TypeError) as error:
            self.logger.warning(error.args[0])
            sleep(2.0)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    dht11 = DHT11(board.D4, logger)

    while True:
        try:
            json_file = dht11.readDHT()

            if not len(json_file) == 0:
                print(json_file['message'])

            sleep(1.5)

        except (RuntimeError, TypeError) as error:
            logger.warning(error.args[0])
            sleep(2.0)

        except KeyboardInterrupt:
            print("\nExiting Program")
            dht11.device.exit()
            break
