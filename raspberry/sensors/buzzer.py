from time import sleep

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone


class Buzzer:
    def __init__(self, pin):
        self.buzzer = TonalBuzzer(pin)

    def play(self, tone, delay):
        if isinstance(tone, float):
            self.buzzer.play(Tone(frequency=tone))
        elif isinstance(tone, int):
            self.buzzer.play(Tone(midi=tone))
        elif isinstance(tone, str):
            self.buzzer.play(Tone(note=tone))
        sleep(delay)

    def stop(self):
        self.buzzer.stop()

    def chime(self):
        self.play("A4", 0.2)
        self.play("B4", 0.2)
        self.play("C4", 0.2)
        self.play("A3", 0.2)


if __name__ == "__main__":
    b = Buzzer(25)

    # Frequency in Hz (Float):
    b.play(220.0, 1.0)

    # MIDI note (Integer):
    b.play(60, 1.0)  # middle C in MIDI notation

    # Representation of musical notes (String):
    b.play("A4", 1.0)

    b.chime()
    b.stop()
