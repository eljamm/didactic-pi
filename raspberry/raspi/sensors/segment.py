import sys
import threading
from collections import deque
from itertools import cycle
from signal import pause

from gpiozero import LEDCharDisplay, LEDCharFont, LEDMultiCharDisplay
from gpiozero.fonts import load_font_7seg, load_font_14seg


class Segment:
    def __init__(self, pins, multi={}, setup=False):
        self.pins = [i for i in pins.values() if i != pins["dp"]]
        self.dp = pins["dp"]

        self.multi = [i for i in multi.values()]
        self.is_scrolling = False

        if setup:
            self.setup()

    def setup(self):
        self.display = LEDCharDisplay(*self.pins, dp=self.dp)

        if len(self.multi) > 0:
            from pkg_resources import resource_stream
            font = {
                7: lambda: load_font_7seg(
                    resource_stream(__name__, 'fonts/7seg.txt')),
                14: lambda: load_font_14seg(
                    resource_stream(__name__, 'fonts/14seg.txt')),
            }[len(self.pins)]()

            self.display._font = LEDCharFont(font)
            self.display = LEDMultiCharDisplay(self.display, *self.multi)

    def cleanup(self):
        self.display.close()

    def clean_str(self, string: str) -> str:
        valid_chars = " abcdefghijklmnopqrstuvwxyz0123456789"
        cleaned = list(string)

        i = 0
        for c in cleaned:
            if c.lower() not in valid_chars:
                cleaned[i] = ""
            i += 1

        return "".join(cleaned)+"      "

    def scroller(self, message, chars=4):
        d = deque(maxlen=chars)
        for c in cycle(message):
            d.append(c)
            if len(d) == chars:
                yield ''.join(d)

    def scroll(self, message):
        self.display.source_delay = 0.5
        self.display.source = self.scroller(message)

        pause()


if __name__ == "__main__":
    seg_pins = {
        "dp": 21,
        "A": 20,
        "B": 16,
        "C": 12,
        "D": 7,
        "E": 8,
        "F": 25,
        "G": 24,
    }
    seg_multi = {
        "dig1": 14,
        "dig2": 15,
        "dig3": 18,
        "dig4": 23,
    }

    segment = Segment(seg_pins, multi=seg_multi, setup=True)
    message = segment.clean_str("Hello, World!")

    while True:
        message = segment.clean_str(
            input("What would you like to print ?\n-> "))

        try:
            t = threading.Thread(target=segment.scroll(message))
            t.start()

        except KeyboardInterrupt:
            i = input("\nRerun or Quit (R/Q) ?\n-> ")

            if i.lower() == "r":
                continue
            else:
                print("\nQuitting Program")
                segment.cleanup()
                break

    sys.exit()
