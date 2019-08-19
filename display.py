import sched
import threading
import time

import config
from PIL import Image, ImageDraw

from atomic_value import AtomicValue
from common import log_paint, log_fw

display_instance = None

if config.USE_EMU:
    import pyglet
    from pyglet.gl import *
    from pyglet import window
    import six
    from pyglet.window import FPSDisplay
else:
    # Import libraries for oled display:
    # https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/overview
    import board
    import busio
    from digitalio import DigitalInOut, Direction, Pull
    import adafruit_ssd1306
    import RPi.GPIO as GPIO

if config.USE_EMU:
    def on_key_press(symbol, modifiers):
        display_instance.handle_button_event(symbol)(pressed=True)
        display_instance.old_on_key_press(symbol, modifiers)


    def on_key_release(symbol, modifiers):
        display_instance.handle_button_event(symbol)(pressed=False)
        # display_instance.old_on_key_release(symbol, modifiers)


    def on_draw():
        display_instance.render()


    def on_close():
        display_instance.on_close()
        display_instance.original_on_close()
else:
    def gpio_callback(channel):
        display_instance.handle_button_event(channel)(pressed=not GPIO.input(channel))


class OledDisplay:
    mutex_disp = threading.Lock()

    def __init__(self):
        global display_instance
        display_instance = self
        self.is_running = AtomicValue(True)
        self.is_painting = AtomicValue(False)
        self.pilimg = Image.new('1', (config.WIDTH, config.HEIGHT))
        self.draw = ImageDraw.Draw(self.pilimg)

        if config.USE_EMU:
            # Create the window using pyglet
            self.window = pyglet.window.Window(visible=False, resizable=True)
            self.old_on_key_press = self.window.on_key_press
            # AttributeError: 'CocoaWindow' object has no attribute 'on_key_release'
            # self.old_on_key_release = self.window.on_key_release
            self.window.on_key_press = on_key_press
            self.window.on_key_release = on_key_release
            self.window.on_draw = on_draw
            self.original_on_close = self.window.on_close
            self.window.on_close = on_close

            checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
            self.background = pyglet.image.TileableTexture.create_for_image(checks)

            # Enable alpha blending, required for image.blit.
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.window.width = config.WIDTH + 64
            self.window.height = config.HEIGHT + 64
            self.window.set_visible()

            self.fps_display = FPSDisplay(self.window)
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
        self.scheduler = sched.scheduler(time.time, time.sleep)
        # First event comes later
        self.sched_event = self.scheduler.enter(1, 1, self.on_sched_event, ())

        t = threading.Thread(target=self.scheduler.run)
        t.start()

    def on_close(self):
        if config.USE_EMU:
            self.is_running.set(False)

    def on_sched_event(self):
        if not self.is_running.get():
            print("Terminating scheduler")
            return
        self.sched_event = self.scheduler.enter(0.05, 1, self.on_sched_event, ())

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
        try:
            return mapping[button]
        except KeyError:
            return self.default_handler

    def clear(self, color=0):
        if config.USE_EMU:
            # TODO
            print("simulated display needs cleaning")
            self.draw.rectangle((0, 0, config.WIDTH, config.HEIGHT), fill=1)
            self.update_image()
        else:
            with self.mutex_disp:
                # Clear display.
                self.disp.fill(color)
                self.disp.show()

    def update_image(self):
        if config.USE_EMU:
            on_draw()
            self.window.clear()
        else:
            self.disp.image(self.pilimg)
            self.disp.show()

    def default_handler(self, pressed):
        print("Unbound key, default handler")

    def on_button_a(self, pressed):
        pass

    def on_button_b(self, pressed):
        pass

    def on_button_c(self, pressed):
        pass

    def on_button_up(self, pressed):
        pass

    def on_button_down(self, pressed):
        pass

    def on_button_left(self, pressed):
        pass

    def on_button_right(self, pressed):
        pass

    def render(self):
        if config.USE_EMU and not self.is_painting.get():
            log_paint.debug("Emu::render()")
            self.is_painting.set(True)
            self.window.clear()
            # TODO: Optimize multiple transforms
            pilbuffer = self.pilimg.tobytes()
            ibuffer = []
            for b in pilbuffer:
                for i in range(8):
                    ibuffer.append(255 if b & 0x80 else 0)
                    b <<= 1
            frame = b''.join(list(map(lambda x: six.int2byte(x), ibuffer)))
            image = pyglet.image.ImageData(self.pilimg.width, self.pilimg.height, 'L', frame, pitch=-self.pilimg.width * 1)
            image.anchor_x = image.width // 2
            image.anchor_y = image.height // 2
            self.background.blit_tiled(0, 0, 0, self.window.width, self.window.height)
            image.blit(self.window.width // 2, self.window.height // 2)
            self.fps_display.draw()
            self.is_painting.set(False)

    @staticmethod
    def run():
        if config.USE_EMU:
            # pyglet.clock.schedule(OledDisplay.update_image)
            pyglet.app.run()
        else:
            try:
                while True:
                    time.sleep(0.2)
            except KeyboardInterrupt:
                if not config.USE_EMU:
                    GPIO.cleanup()


if __name__ == "__main__":
    print("Starting saat display test")
    display = OledDisplay()
    display.draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  # Up
    display.draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  # left
    display.draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0)  # right
    display.draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0)  # down
    display.draw.rectangle((20, 22, 40, 40), outline=255, fill=0)  # center
    display.draw.ellipse((70, 40, 90, 60), outline=255, fill=0)  # A button
    display.draw.ellipse((100, 20, 120, 40), outline=255, fill=0)  # B button
    display.update_image()

    display.run()
