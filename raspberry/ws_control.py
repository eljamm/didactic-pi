import asyncio
import json
import logging
import os
import threading

import board
import coloredlogs
import digitalio
import websocket

from sensors import DHT11, LCD, ArrayLED, DPad, Joystick, Matrix, Buzzer
from utils import async_receive, run


class RaspberryClient:
    def __init__(self, server, port, pi_name):
        # --- Websocket --- #
        websocket.enableTrace(True)

        self.url = "ws://%s:%s/ws/%s/" % (server, port, pi_name)
        self.ws = websocket.create_connection(self.url)

        # --- Logger --- #
        self.logger = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG', logger=self.logger)

        # --- DHT11 --- #
        self.dht11 = DHT11(board.D14, self.logger)

        # --- 8x8 Matrix --- #
        mat_rows = [21, 8, 26, 12, 10, 19, 9, 6]
        mat_cols = [7, 11, 5, 20, 13, 16, 25, 24]

        self.mat8x8 = Matrix(mat_rows, mat_cols)

        # --- D-Pad --- #
        dpad_dirs = {
            'up': 4,
            'down': 3,
            'left': 2,
            'right': 17
        }

        self.dpad = DPad(dpad_dirs, self.mat8x8)

        # --- LED Array --- #
        blue_array = [21, 20, 16, 12, 7, 8, 25, 24, 23, 18]
        red_array = [26, 19, 13, 6, 5, 11, 9, 10, 22, 27]

        self.array_led = ArrayLED(blue_array, red_array)

        # --- LCD Display --- #
        lcd_pins = {
            'rs': digitalio.DigitalInOut(board.D19),
            'en': digitalio.DigitalInOut(board.D26),
            'd4': digitalio.DigitalInOut(board.D7),
            'd5': digitalio.DigitalInOut(board.D12),
            'd6': digitalio.DigitalInOut(board.D16),
            'd7': digitalio.DigitalInOut(board.D20),
            'backlight': digitalio.DigitalInOut(board.D21)
        }

        lcd_columns = 16
        lcd_rows = 2

        self.lcd = LCD(lcd_pins, lcd_columns, lcd_rows)

        # --- Joystick --- #
        adc_pins = {
            'clk': 18,
            'do': 27,
            'di': 22,
            'cs': 17,
        }

        joy_dirs = {
            'LEFT': 24,
            'DOWN': 25,
            'UP': 14,
            'RIGHT': 15,
            'CENTER': 23
        }

        self.joystick = Joystick(adc_pins, joy_dirs)

        # --- Buzzer --- #
        midi_pins = {
            "C4": 2,
            "D4": 3,
            "E4": 4,
            "F4": 17,
            "G4": 27,
        }

        self.buzzer = Buzzer(25, midi_pins)

        self.sensors = [self.logger, self.dht11, self.mat8x8, self.dpad,
                        self.array_led, self.lcd, self.joystick, self.buzzer]


if __name__ == "__main__":
    # --- Raspi Config --- #
    server = "192.168.1.52"
    port = "8000"
    pi_name = "IOT1"

    raspi = RaspberryClient(server, port, pi_name)

    # --- Start App --- #
    while True:
        try:
            # Async Read from Websocket
            data = asyncio.run(async_receive(raspi.ws))
            json_file = json.loads(data)

            # Update Data
            sensor = json_file['sensor']
            raspi.message = message = json_file['message']
            raspi.message_type = message_type = json_file['message_type']

            t = threading.Thread(target=run,
                                 args=(sensor, raspi),
                                 daemon=True)

            if message == "start" and message_type == "command":
                print("Starting Thread")
                t.start()

            elif message == "exit" and message_type == "command":
                print("\nClosing Program")
                raspi.ws.close()
                break

        except KeyboardInterrupt:
            print("\nClosing Program")
            os._exit(0)
