from gpiozero import OutputDevice
from time import sleep


class Relay:
    def __init__(self, pins, setup=False):
        self.COM_PIN = pins["COM"]
        self.SWITCH_PIN = pins["SWITCH"]

        if setup:
            self.setup()

    def setup(self):
        self.com = OutputDevice(self.COM_PIN)
        self.switch = OutputDevice(self.SWITCH_PIN)

        self.devices = [self.com, self.switch]

    def cleanup(self):
        if len(self.devices) > 0:
            for device in self.devices:
                device.close()

    def toggle_switch(self, delay):
        if self.switch.is_active:
            self.switch.off()
            sleep(delay)
        else:
            self.switch.on()
            sleep(delay)


if __name__ == "__main__":
    pins = {
        "COM": 21,      # Common pin
        "SWITCH": 20    # Relay coil switch
    }

    sleep(2.0)

    relay = Relay(pins, setup=True)

    relay.com.on()  # Power COM on from GPIO
    sleep(2.0)

    # Switch between LEDs
    for i in range(5):
        relay.switch.on()
        sleep(1.0)
        relay.switch.off()
        sleep(1.0)

    relay.com.off()  # Power COM off from GPIO

    relay.cleanup()
