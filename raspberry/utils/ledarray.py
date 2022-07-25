from gpiozero import LED
from time import sleep


class ArrayLED:
    def __init__(self, blue, red):
        self.blue = blue
        self.red = red
        self.array = [blue, red]

    def cleanup(self):
        self.clear_leds()
        for array in self.array:
            for led in array:
                led.close()

    def clear_leds(self):
        for array in self.array:
            for led in array:
                led.off()

    def scan(self):
        for array in self.array:
            for led in array:
                led.on()
                sleep(0.5)
                led.off()

    def processArray(self, message):
        blink_list = []
        if isinstance(message, list):
            for i in range(len(message)):
                j = 0
                for state in message[i]:
                    if state == "inactive":
                        self.array[i][j].off()
                    elif state == "active":
                        self.array[i][j].on()
                    elif state == "blink":
                        blink_list.append(self.array[i][j])
                    j += 1
        return blink_list

    def blinkLEDs(self, blink_list, on_time, off_time):
        for led in blink_list:
            led.on()
        sleep(on_time)
        for led in blink_list:
            led.off()
        sleep(off_time)


if __name__ == "__main__":
    blue_array = [LED(21), LED(20), LED(16), LED(12), LED(7),
                  LED(8), LED(25), LED(24), LED(23), LED(18)]

    red_array = [LED(26), LED(19), LED(13), LED(6), LED(5),
                 LED(11), LED(9), LED(10), LED(22), LED(27)]

    array_led = ArrayLED(blue_array, red_array)

    state_array = [["active", "inactive", "blink", "inactive", "active", "inactive", "blink", "active", "inactive", "active"], [
        "blink", "inactive", "active", "active", "inactive", "active", "blink", "inactive", "active", "inactive"]]

    try:
        blink_list = array_led.processArray(state_array)
        sleep(3.0)

        while True:
            array_led.blinkLEDs(blink_list, 1.0, 2.0)

    except KeyboardInterrupt:
        print("\nExiting Program")
        array_led.cleanup()
