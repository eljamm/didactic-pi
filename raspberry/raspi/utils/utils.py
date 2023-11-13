import asyncio
import re
import threading
from time import sleep

from raspi.sensors import DHT11


async def async_receive(ws):
    result = await asyncio.get_event_loop().run_in_executor(None, ws.recv)
    return result


def run(sensor, pi):
    (logger, dht11, mat8x8, dpad, array_led,
     lcd, joystick, buzzer, segment, relay, ultra) = pi.sensors

    # --- Sensor Regex --- #
    sensor_is_dht = re.search(".*dht11-.*", sensor)
    sensor_is_led = re.search(".*ledarray-.*", sensor)
    sensor_is_lcd = re.search(".*lcd-.*", sensor)
    sensor_is_mat = re.search(".*8x8matrix-.*", sensor)
    sensor_is_joy = re.search(".*joystick-.*", sensor)
    sensor_is_buz = re.search(".*buzzer-.*", sensor)
    sensor_is_seg = re.search(".*7segment.*", sensor)
    sensor_is_rel = re.search(".*relay-.*", sensor)
    sensor_is_ult = re.search(".*ultrasonic.*", sensor)

    # --- Extra Regex --- #
    extra_is_gauge = re.search(".*gauge.*", sensor)
    extra_is_lcd = re.search(".*lcd.*", sensor)
    extra_is_shape = re.search(".*shape.*", sensor)
    extra_is_dpad = re.search(".*dpad.*", sensor)
    extra_is_leds = re.search(".*leds.*", sensor)
    extra_is_mat = re.search(".*matrix.*", sensor)
    extra_is_alarm = re.search(".*alarm.*", sensor)
    extra_is_midi = re.search(".*midi.*", sensor)

    # --- Setup --- #
    # DHT11
    if sensor_is_dht:
        dht11 = DHT11(dht11.pin, logger)

    # 8x8 LED Matrix
    elif sensor_is_mat:
        mat8x8.setup()

        # D-Pad
        if extra_is_dpad:
            dpad.setup()

    # LED Array
    elif sensor_is_led:
        array_led.setup()

    # LCD Display
    elif sensor_is_lcd:
        lcd.on()

    # Joystick
    elif sensor_is_joy:
        joystick.setup()

        # Matrix
        if extra_is_mat:
            mat8x8.setup()
            mat8x8.selectPixel(0, 0)

        # LEDs
        elif extra_is_leds:
            joystick.setupLEDs()

    # Buzzer
    elif sensor_is_buz:
        buzzer.setup()

        # Midi
        if extra_is_midi:
            buzzer.setupMidi()

    # Segment
    elif sensor_is_seg:
        segment.setup()

    # Relay
    elif sensor_is_rel:
        relay.setup()
        relay.com.on()  # Power COM on from GPIO

    # Ultrasonic
    elif sensor_is_ult:
        ultra.setup()

    while True:
        message = pi.message
        message_type = pi.message_type

        sensor_is_seg = re.search(".*7segment.*", pi.sensor)

        # --- Stop --- #
        if message == "stop" and message_type == "command":
            print("Stopping Thread")

            # DHT11
            if sensor_is_dht:
                dht11.device.exit()

            # 8x8 LED Matrix
            elif sensor_is_mat:
                mat8x8.clearMatrix()

                # D-Pad
                if extra_is_dpad:
                    dpad.cleanup()

            # LED Array
            elif sensor_is_led:
                array_led.cleanup()

            # LCD Display
            elif sensor_is_lcd:
                lcd.clear()
                lcd.off()

            # Joystick
            elif sensor_is_joy:
                joystick.cleanup()

                # Matrix
                if extra_is_mat:
                    mat8x8.clearMatrix()
                    sleep(3.0)

                # LEDs
                elif extra_is_leds:
                    joystick.cleanupLEDs()

            # Buzzer
            elif sensor_is_buz:
                # Alarm
                if extra_is_alarm:
                    buzzer.cleanup()

                # Midi
                elif extra_is_midi:
                    buzzer.cleanupMidi()

            # Segment
            elif sensor_is_seg:
                segment.cleanup()

            # Relay
            elif sensor_is_rel:
                relay.com.off()  # Power COM off from GPIO
                relay.cleanup()

            # Ultrasonic
            elif sensor_is_ult:
                ultra.cleanup()

            break

        # --- Process --- #
        try:
            # DHT11
            if sensor_is_dht:
                if extra_is_gauge:
                    dht11.processDHT(pi.ws, 1.5)
                elif extra_is_lcd:
                    dht11.processDHT_LCD(lcd, 2.0)

            # 8x8 LED Matrix
            elif sensor_is_mat:
                if extra_is_shape:
                    mat8x8.processMatrix(message)
                elif extra_is_dpad:
                    dpad.processDPad()

            # LED Array
            elif sensor_is_led:
                blink_list = array_led.processArray(message)
                array_led.blinkLEDs(blink_list, 1.0, 1.0)

            # LCD Display
            elif sensor_is_lcd:
                if message_type != "command":
                    lcd.processLCD(message, 3.0, 1.5)

            # Joystick
            elif sensor_is_joy:
                if extra_is_leds:
                    joystick.processJoy()
                elif extra_is_mat:
                    joystick.processJoyMatrix(mat8x8)

            # Buzzer
            elif sensor_is_buz:
                if extra_is_alarm:
                    if message == "play":
                        buzzer.alarm(10, 0.5)
                        sleep(2.0)
                    elif message == "stop":
                        buzzer.stop()

                elif extra_is_midi:
                    buzzer.processMidi(0.2)

                    if re.search("^play-.*", message):
                        key = message.split("-")[1]
                        index = 0

                        for item in buzzer.midi_keys:
                            if key == item:
                                buzzer.play(index+57, 0.1)
                            else:
                                index += 1

                    elif message == "stop":
                        buzzer.stop()

            # Segment
            elif sensor_is_seg and message_type == "data":
                stop_event = threading.Event()
                clean_msg = segment.clean_str(message)

                def run_scroll(stop_event: threading.Event):
                    if not stop_event.is_set():
                        segment.scroll(clean_msg)

                t = threading.Thread(target=run_scroll, args=(stop_event,))
                t.start()

                pi.sensor = "none"

            # Relay
            elif sensor_is_rel:
                if extra_is_alarm:
                    relay.toggle_switch(1.0)

            # Ultrasonic
            elif sensor_is_ult:
                ultra.process(pi.ws, 1.5)

        except RuntimeError as error:
            logger.warning(error.args[0])
            sleep(2.0)
            continue
