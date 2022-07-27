import _thread
import asyncio
import json
import logging
import re
import sys
import textwrap
import threading
from time import sleep

import adafruit_character_lcd.character_lcd as character_lcd
import adafruit_dht
import board
import coloredlogs
import digitalio
import websocket
from gpiozero import LED

from utils.dht11 import DHT11
from utils.lcd import LCD
from utils.ledarray import ArrayLED
from utils.ledmatrix import Matrix


def initial_setup():
    # --- Logger --- #
    global logger

    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    # --- DHT11 --- #
    global dht11

    dht11 = DHT11(board.D14, logger)

    # --- 8x8 Matrix --- #
    global mat8x8

    mat_rows = [21, 8, 26, 12, 10, 19, 9, 6]
    mat_cols = [7, 11, 5, 20, 13, 16, 25, 24]

    mat8x8 = Matrix(mat_rows, mat_cols)

    # --- LED Array --- #
    global array_led

    blue_array = [LED(21), LED(20), LED(16), LED(12), LED(7),
                  LED(8), LED(25), LED(24), LED(23), LED(18)]

    red_array = [LED(26), LED(19), LED(13), LED(6), LED(5),
                 LED(11), LED(9), LED(10), LED(22), LED(27)]

    array_led = ArrayLED(blue_array, red_array)

    # --- LCD Display --- #
    global lcd

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

    lcd = LCD(lcd_pins, lcd_columns, lcd_rows)


async def my_receive():
    result = await asyncio.get_event_loop().run_in_executor(None, ws.recv)
    return result


def run(sensor, stop_event):
    t = threading.current_thread()
    reg_dht = re.compile(".*dht11.*")
    reg_lcd = re.compile(".*lcd.*")

    # --- Setup --- #
    if reg_dht.match(sensor):
        dht11 = DHT11(board.D4, logger)
    if reg_lcd.match(sensor):
        lcd.on()
    if sensor == "mt-8x8matrix":
        mat8x8.setup()

    while not stop_event.is_set():
        # --- Clear --- #
        if message == "stop" and message_type == "command":
            if reg_dht.match(sensor):
                dht11.device.exit()
            if reg_lcd.match(sensor):
                lcd.clear()
                lcd.off()
            if sensor == "mt-8x8matrix":
                mat8x8.clearMatrix()
            elif sensor == "mt-ledarray":
                array_led.clear_leds()
            sensor = "none"

        # --- Process --- #
        try:
            if sensor == "mt-dht11-gauge":
                dht11.processDHT(ws, 1.5)
            
            elif sensor == "mt-dht11-lcd":
                dht11.processDHT_LCD(lcd, 2.0)

            elif sensor == "mt-8x8matrix":
                mat8x8.processMatrix(message)

            elif sensor == "mt-ledarray":
                blink_list = array_led.processArray(message)
                array_led.blinkLEDs(blink_list, 1.0, 1.0)

            elif sensor == "mt-lcd":
                if message_type != "command":
                    lcd.processLCD(message, 3.0, 1.5)

        except RuntimeError as error:
            logger.warning(error.args[0])
            sleep(2.0)
            continue


if __name__ == "__main__":
    websocket.enableTrace(True)

    url = "ws://192.168.1.52:8000/ws/IOT1/"
    ws = websocket.create_connection(url)

    initial_setup()

    while True:
        try:
            data = asyncio.run(my_receive())
            json_file = json.loads(data)

            sensor = json_file['sensor']
            message = json_file['message']
            message_type = json_file['message_type']

            stop_event = threading.Event()
            t = threading.Thread(target=run,
                                 args=(sensor, stop_event),
                                 daemon=True)

            if message == "start" and message_type == "command":
                print("Starting Thread")
                t.start()

            elif message == "stop" and message_type == "command":
                print("Stopping Thread")
                stop_event.set()
                ws.close()
                ws.connect(url)

            elif message == "exit" and message_type == "command":
                print("\nClosing Program")
                stop_event.set()
                ws.close()
                break

        except KeyboardInterrupt:
            print("\nClosing Program")
            stop_event.set()
            ws.close()
            break
    sys.exit()
