from time import sleep

import config
from PIL import Image, ImageDraw
if config.USE_EMU:
    import pyglet
    from pyglet.gl import *
else:
    # Import libraries for oled display:
    # https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/overview
    import board
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import adafruit_ssd1306
    import RPi.GPIO as GPIO


if config.USE_EMU:
    @window.event
    def pyglet_on_key_press(self, symbol, modifiers):
        print(f"Received keyboard callback {symbol}:{modifiers}")
        self._resolve(symbol)
else:
    def gpio_callback(channel):
        print(f"Received falling gpio on channel {channel}, instance is {display_instance}")
        display_instance.handle_button_event(channel)(pressed=not GPIO.input(channel))


class SaatDisplay:
    def __init__(self):
        global display_instance
        display_instance = self
        self.pilimg = Image.new('1', (config.WIDTH, config.HEIGHT))
        self.draw = ImageDraw.Draw(self.pilimg)

        if config.USE_EMU:
            # Create the window using pyglet
            import six

            self.window = pyglet.window.Window(visible=False, resizable=True)
        else:
            GPIO.setmode(GPIO.BCM)

            # Create the I2C interface.
            self.i2c = busio.I2C(board.SCL, board.SDA)
            # Create the SSD1306 OLED class.
            self.disp = adafruit_ssd1306.SSD1306_I2C(config.WIDTH, config.HEIGHT, self.i2c)

            for button in config.ALL_BUTTONS:
                GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(button, GPIO.BOTH, callback=gpio_callback, bouncetime=20)

        self.clear()


    def handle_button_event(self, button):
        mapping = {
            config.BUTTON_A: self.on_button_a,
            config.BUTTON_B: self.on_button_b,
            config.BUTTON_C: self.on_button_c,
            config.BUTTON_UP: self.on_button_up,
            config.BUTTON_DOWN: self.on_button_down,
            config.BUTTON_LEFT: self.on_button_left,
            config.BUTTON_RIGHT: self.on_button_right,
        }
        return mapping[button]

    def clear(self, color=0):
        if config.USE_EMU:
            # TODO
            print("simulated display needs cleaning")
        else:
            # Clear display.
            self.disp.fill(color)
            self.disp.show()

    def update(self):
        if config.USE_EMU:
            print("do simulated")
        else:
            self.disp.image(self.pilimg)
            self.disp.show()

    def on_button_a(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button A")
        display.draw.ellipse((70, 40, 90, 60), outline=255, fill=1 if pressed else 0)  # A button
        display.update()

    def on_button_b(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button B")
        display.draw.ellipse((100, 20, 120, 40), outline=255, fill=1 if pressed else 0)  # B button
        display.update()

    def on_button_c(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button C")
        display.draw.rectangle((20, 22, 40, 40), outline=255, fill=1 if pressed else 0)  # center
        display.update()

    def on_button_up(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button UP")
        display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=1 if pressed else 0)  # Up
        display.update()

    def on_button_down(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button DOWN")
        display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=1 if pressed else 0)  # down
        display.update()

    def on_button_left(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button LEFT")
        display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=1 if pressed else 0)  # left
        display.update()

    def on_button_right(self, pressed):
        print(f"{'Pressed' if pressed else 'Released'} - Button RIGHT")
        display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=1 if pressed else 0)  # right
        display.update()


if __name__ == "__main__":
    print("Starting saat display test")
    display = SaatDisplay()
    display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  # Up
    display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  # left
    display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) # right
    display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) # down
    display.draw.rectangle((20, 22, 40, 40), outline=255, fill=0)  # center
    display.draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button
    display.draw.ellipse((100, 20, 120, 40), outline=255, fill=0)  # B button
    display.update()

    try:
        while True:
            sleep(0.2)
    except KeyboardInterrupt:
        if not config.USE_EMU:
            GPIO.cleanup()
