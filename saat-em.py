import platform
import threading
from time import sleep

import pyglet


class OledDisplay:
    RASPI = platform.machine() == "armv7l" and platform.system() == "Linux"
    WIDTH = 128
    HEIGHT = 64
    if RASPI:
        # Import libraries for oled display:
        # https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/overview
        import board
        import busio
        from digitalio import DigitalInOut, Direction, Pull
        import adafruit_ssd1306
    else:
        import pyglet
        from pyglet.gl import *
        import six

    def __init__(self):
        self.image = Image.new('1', (self.WIDTH, self.HEIGHT))
        self.draw = ImageDraw.Draw(self.image)
        if self.RASPI:
            # Create the I2C interface.
            self.i2c = busio.I2C(board.SCL, board.SDA)
            # Create the SSD1306 OLED class.
            self.disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

            # Input pins:
            button_A = DigitalInOut(board.D5)
            button_A.direction = Direction.INPUT
            button_A.pull = Pull.UP

            button_B = DigitalInOut(board.D6)
            button_B.direction = Direction.INPUT
            button_B.pull = Pull.UP

            button_L = DigitalInOut(board.D27)
            button_L.direction = Direction.INPUT
            button_L.pull = Pull.UP

            button_R = DigitalInOut(board.D23)
            button_R.direction = Direction.INPUT
            button_R.pull = Pull.UP

            button_U = DigitalInOut(board.D17)
            button_U.direction = Direction.INPUT
            button_U.pull = Pull.UP

            button_D = DigitalInOut(board.D22)
            button_D.direction = Direction.INPUT
            button_D.pull = Pull.UP

            button_C = DigitalInOut(board.D4)
            button_C.direction = Direction.INPUT
            button_C.pull = Pull.UP

            # Clear display.
            self.disp.fill(0)
            self.disp.show()
        else:
            # TODO: Keyboard
            print("Simulated display")
            self.window = pyglet.window.Window(visible=False, resizable=True)

    def flush(self):
        if self.RASPI:
            self.disp.image(self.image)
            disp.show()
        else:
            self.panel.configure(image=self.image)


if __name__ == "__main__":
    oled = OledDisplay()
    sleep(1)
    oled.draw.rectangle((1, 1, 40, 20), outline=255, fill=1)
    oled.flush()
