from time import sleep

from gpiozero import TonalBuzzer, Button
from gpiozero.tones import Tone


class Buzzer:
    def __init__(self, pin, midi_pins={}, setup=False):
        self.pin = pin
        self.midi_pins = midi_pins
        self.midi_keys = [
            "w",
            "x", "s", "c", "d", "v", "f", "b",
            "n", "j", ",", "k", ";",
            "a", "é", "z", "\"", "e", "'", "r",
            "t", "-", "y", "è", "u"
        ]

        if setup:
            self.setup()

    def setup(self):
        self.buzzer = TonalBuzzer(self.pin)

    def cleanup(self):
        self.buzzer.close()

    def setupMidi(self):
        self.midi_buttons = []

        if len(self.midi_pins) > 0:
            for value in self.midi_pins.values():
                self.midi_buttons.append(Button(value))

    def cleanupMidi(self):
        for note in self.midi_buttons:
            note.close()

        self.buzzer.close()

    def processMidi(self, delay):
        for key in self.midi_buttons:
            if key.is_pressed:
                self.playMidi(key, delay)
            else:
                self.stop()

    def play(self, tone, delay=1.0):
        if isinstance(tone, float):
            # Min frequency is 220.0 and max is 880.0
            self.buzzer.play(Tone(frequency=tone))
        elif isinstance(tone, int):
            # Min tone is 57 and max is 81
            self.buzzer.play(Tone(midi=tone))
        elif isinstance(tone, str):
            # Min note is A3 and max is A5
            self.buzzer.play(Tone(note=tone))
        sleep(delay)

    def playMidi(self, button, delay):
        note = int(str(button.pin).split("GPIO")[1])

        for key, value in self.midi_pins.items():
            if note == value:
                self.play(key, delay)

    def stop(self):
        self.buzzer.stop()

    def chime(self):
        self.play("A4", 0.2)
        self.play("B4", 0.2)
        self.play("C4", 0.2)
        self.play("A3", 0.2)
        self.stop()

    def alarm(self, repeat, delay):
        for i in range(repeat):
            self.play(220.0, delay/2)
            self.play(420.0, delay/2)
        self.stop()


if __name__ == "__main__":
    midi_pins = {
        "C4": 2,
        "D4": 3,
        "E4": 4,
        "F4": 17,
        "G4": 27,
    }

    b = Buzzer(25, midi_pins, True)

    try:
        # --- Buzzing Examples --- #

        # Frequency in Hz (Float):
        b.play(220.0, 1.0)

        # MIDI note (Integer):
        b.play(60, 1.0)  # middle C in MIDI notation

        # Representation of musical notes (String):
        b.play("A4", 1.0)

        b.stop()
        sleep(2.0)

        # Alarm
        b.alarm(10, 0.5)

        sleep(2.0)

        # Chime
        b.chime()

        # --- Midi Keyboard --- #

        b.setupMidi()
        while True:
            b.processMidi(0.2)

        b.cleanupMidi()

    except KeyboardInterrupt:
        print("\nQuitting Program")
        b.stop()
