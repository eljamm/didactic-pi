import _thread
import asyncio
import json
import logging
import sys
import threading
from time import sleep

import adafruit_dht
import board
import coloredlogs
import RPi.GPIO as GPIO
import websocket

from utils.dht11 import processDHT
from utils.ledmatrix import Matrix


class Globals:
    def __init__(self):
        ## Logger ##
        logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=logger)

        ## Sensors ##
        # DHT11
        dht11 = adafruit_dht.DHT11(board.D19, use_pulseio=False)

        # 8x8 Matrix
        mat_rows = [7, 18, 9, 24, 2, 10, 3, 27]
        mat_cols = [23, 4, 17, 8, 22, 25, 15, 14]

        mat8x8 = Matrix(mat_rows, mat_cols)

        ## Attributes ##
        self.logger = logger
        self.dht11 = dht11
        self.mat8x8 = mat8x8


async def my_receive():
    result = await asyncio.get_event_loop().run_in_executor(None, ws.recv)
    return result


def run(sensor, stop_event):
    t = threading.current_thread()
    g.mat8x8.setup()

    while not stop_event.is_set():
        if message == "stop":
            stop_event.set()
            g.mat8x8.clearMatrix()

        try:
            if sensor == "mt-dht11":
                processDHT(ws, g.dht11, g.logger)

            elif sensor == "mt-8x8matrix":
                g.mat8x8.processMatrix(message)

        except RuntimeError as error:
            g.logger.warning(error.args[0])
            sleep(2.0)


if __name__ == "__main__":
    websocket.enableTrace(True)

    url = "ws://192.168.1.52:8000/ws/IOT1/"
    ws = websocket.create_connection(url)

    g = Globals()

    while True:
        try:
            data = asyncio.run(my_receive())
            json_file = json.loads(data)

            sensor = json_file['sensor']
            message = json_file['message']

            stop_event = threading.Event()
            t = threading.Thread(target=run,
                                 args=(sensor, stop_event),
                                 daemon=True)

            if message == "start":
                print("Starting Thread")
                t.start()

            elif message == "stop":
                print("Stopping Thread")
                ws.close()
                ws.connect(url)

        except KeyboardInterrupt:
            print("\nClosing Program")
            ws.close()
            sys.exit()
