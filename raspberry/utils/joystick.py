#!/usr/bin/env python
#
# Modified version of Heinrich Hartmann's RPi_ADC8032 code :
# https://gist.github.com/HeinrichHartmann/27f33798d12317575c6c
#

from time import sleep
import os
import RPi.GPIO as GPIO
from gpiozero import LED, Button


class Joystick:
    def __init__(self, adc_pins, dir_pins):
        self.di = adc_pins['di']
        self.do = adc_pins['do']
        self.clk = adc_pins['clk']
        self.cs = adc_pins['cs']

        self.dir_pins = dir_pins
        self.LEFT = dir_pins['LEFT']
        self.DOWN = dir_pins['DOWN']
        self.UP = dir_pins['UP']
        self.RIGHT = dir_pins['RIGHT']
        self.CENTER = Button(dir_pins['CENTER'])

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        # set up the SPI interface pins
        GPIO.setup(self.di,  GPIO.OUT)
        GPIO.setup(self.do,  GPIO.IN)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.cs,  GPIO.OUT)

    # read SPI data from ADC8032
    def getADC(self, channel):
        # 1. CS LOW.
        GPIO.output(self.cs, True)      # clear last transmission
        GPIO.output(self.cs, False)     # bring CS low

        # 2. Start clock
        GPIO.output(self.clk, False)    # start clock low

        # 3. Input MUX address
        for i in [1, 1, channel]:  # start bit + mux assignment
            if (i == 1):
                GPIO.output(self.di, True)
            else:
                GPIO.output(self.di, False)

            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            GPIO.output(self.clk, True)
            GPIO.output(self.clk, False)
            ad <<= 1  # shift bit
            if (GPIO.input(self.do)):
                ad |= 0x1  # set first bit

        # 5. reset
        GPIO.output(self.cs, True)

        return ad

    def setupDPAD(self):
        self.setup()

        for pin in self.dir_pins.values():
            GPIO.setup(pin,  GPIO.OUT)

    def processDPAD(self):
        Y = self.getADC(0)
        X = self.getADC(1)

        print("X[1]: %s\t Y[0]: %s" % (X, Y))

        if self.CENTER.is_pressed:
            self.all_on()
            print("All LEDs ON")

        else:
            if X > 250:
                GPIO.output(self.LEFT, True)
            elif X < 20:
                GPIO.output(self.RIGHT, True)
            else:
                GPIO.output(self.LEFT, False)
                GPIO.output(self.RIGHT, False)

            if Y > 250:
                GPIO.output(self.DOWN, True)
            elif Y < 20:
                GPIO.output(self.UP, True)
            else:
                GPIO.output(self.UP, False)
                GPIO.output(self.DOWN, False)

        sleep(1.0)

    def all_on(self):
        for pin in self.dir_pins.values():
            GPIO.output(pin, True)


if __name__ == "__main__":

    adc_pins = {
        'clk': 18,
        'do': 27,
        'di': 22,
        'cs': 17,
    }

    dir_pins = {
        'LEFT': 24,
        'DOWN': 25,
        'UP': 14,
        'RIGHT': 15,
        'CENTER': 23
    }

    joy = Joystick(adc_pins, dir_pins)
    joy.setupDPAD()

    try:
        while True:
            joy.processDPAD()

    except KeyboardInterrupt:
        print("\nQuitting Program")
