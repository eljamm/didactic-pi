import json
import logging
from time import sleep

import adafruit_dht
import board
import coloredlogs
import RPi.GPIO as GPIO


def readDHT(dht11, logger):
    try:
        temp_c = dht11.temperature
        temp_f = temp_c * (9 / 5) + 32
        hum = dht11.humidity
        message = "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
            temp_f, temp_c, hum)

        return [message, temp_c, temp_f, hum]

    except TypeError as error:
        logger.warning(error.args[0])


def processDHT(ws, dht11, logger):
    message, temp_c, temp_f, hum = readDHT(dht11, logger)

    ws.send(json.dumps({
        'sensor': 'dht11',
        'message': message,
        'temp': temp_c,
        'hum': hum
    }))

    sleep(1.5)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    dhtDevice = adafruit_dht.DHT11(board.D19, use_pulseio=False)

    while True:
        try:
            message, temp_c, temp_f, hum = readDHT(dhtDevice)

            print(message)
            sleep(2.0)

        except RuntimeError as error:
            logger.warning(error.args[0])

        except KeyboardInterrupt:
            print("\nExiting Program")
            GPIO.cleanup()
            break
