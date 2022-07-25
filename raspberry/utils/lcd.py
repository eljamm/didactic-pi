from time import sleep

import adafruit_character_lcd.character_lcd as character_lcd
import board
import digitalio


class LCD:
    def __init__(self, pins, columns, rows):
        rs = pins['rs']
        en = pins['en']
        d4 = pins['d4']
        d5 = pins['d5']
        d6 = pins['d6']
        d7 = pins['d7']
        backlight = pins['backlight']

        self.lcd = character_lcd.Character_LCD_Mono(
            rs, en, d4, d5, d6, d7, columns, rows, backlight
        )

        self.off()

    def scroll(self, message):
        self.display(message)
        sleep(1.0)

        for i in range(len(message)):
            sleep(0.5)
            self.lcd.move_left()

        sleep(1.0)
        self.clear()

    def display(self, message):
        self.lcd.message = message

    def on(self):
        self.lcd.backlight = True

    def off(self):
        self.lcd.backlight = False

    def clear(self):
        self.lcd.clear()

    def processLCD(self, message):
        self.clear()
        self.display(message)
        sleep(3.0)
        self.scroll(message)
        sleep(1.5)


if __name__ == "__main__":
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

    try:
        lcd.on()
        lcd.display("Hello, World :)")

        sleep(3.0)

        msg = "Arduino or Raspberry ?"
        if len(msg) > 16:
            # Keep scrolling message
            while True:
                lcd.scroll(msg)
        else:
            # Display message
            lcd.clear()
            lcd.display(msg)

        sleep(3.0)

        # Exit
        print("\nExiting Program")
        lcd.clear()
        lcd.off()

    except KeyboardInterrupt:
        print("\nExiting Program")
        lcd.clear()
        lcd.off()
