import sched
import threading
import time

import config
from PIL import Image, ImageDraw

from atomic_value import AtomicValue
from common import log_paint, log_fw

display_instance = None

USE_MICRO = True

if config.USE_EMU:
    import pyglet
    from pyglet.gl import *
    from pyglet import window
    from struct import pack
    from pyglet.window import FPSDisplay
else:
    # Import libraries for oled display:
    # https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/overview
    import board
    import busio
    from digitalio import DigitalInOut, Direction, Pull

    if USE_MICRO:
        import adafruit_ssd1306
    else:
        import Adafruit_SSD1306
    import RPi.GPIO as GPIO

    RST = 24

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


def dump_pilbuffer(buffer):
    s = ""
    lines = 0
    for i in range(0, len(buffer)):
        if i > 0 and (i % 16) == 0:
            print(s)
            s = ""
            lines += 1
        b = buffer[i]
        for bit in range(8):
            s += "*" if b & 0x80 else "."
            b <<= 1
    print(f"Length: {len(buffer)} Lines: {lines}")


class OledDisplay:
    mutex_disp = threading.Lock()
    _external_frame_source = None

    def __init__(self):
        global display_instance
        display_instance = self
        self.is_running = AtomicValue(True)
        self.is_painting = AtomicValue(False)
        self.pilimg = Image.new('1', (config.WIDTH, config.HEIGHT))
        self.draw = ImageDraw.Draw(self.pilimg)

        if config.SHOW_STATS:
            # Performance counters
            self._frames = 0
            self._started_at = None
            self._last_report = 0
            self._last_report_at = None
            self._avg_lock = 0
            self._avg_render = 0
            self._avg_write = 0

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
            if USE_MICRO:
                self.disp = adafruit_ssd1306.SSD1306_I2C(config.WIDTH, config.HEIGHT, self.i2c)
            else:
                self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
                self.disp.begin()

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
        self.sched_event = self.scheduler.enter(0.02, 1, self.on_sched_event, ())

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

    def set_external_framer(self, frame_source_func):
        self._external_frame_source = frame_source_func

    def clear(self, color=0):
        if config.USE_EMU:
            # TODO Clean up for emu
            self.draw.rectangle((0, 0, config.WIDTH, config.HEIGHT), fill=1)
            self.update_image()
        else:
            with self.mutex_disp:
                # Clear display.
                if USE_MICRO:
                    self.disp.fill(color)
                    self.disp.show()
                else:
                    self.disp.clear()
                    self.disp.display()

    def _inc_frame(self, enter, start, render, end):
        if config.SHOW_STATS:
            self._avg_lock = ((self._avg_lock * self._frames) + (start - enter)) / (self._frames + 1)
            self._avg_render = ((self._avg_render * self._frames) + (render - start)) / (self._frames + 1)
            self._avg_write = ((self._avg_write * self._frames) + (end - render)) / (self._frames + 1)
            self._frames += 1
            if self._started_at is None:
                self._started_at = enter
            if self._last_report_at is None:
                self._last_report_at = enter
                self._last_report = 0
            elif (end - self._last_report_at) >= 1.0:
                frames_since = self._frames - self._last_report
                log_paint.info(
                    f"FPS: {frames_since / (end - self._last_report_at):4.2f} {self._frames / (end - self._started_at):4.2f} Time to lock: {self._avg_lock:4.3f} render: {self._avg_render:4.3f} write: {self._avg_write:4.3f}")
                self._last_report_at = end
                self._last_report = self._frames

    def update_image(self):
        if config.USE_EMU:
            pass
            # on_draw()
        else:
            enter = time.perf_counter()
            with self.mutex_disp:
                start = time.perf_counter()
                self.disp.buf = self.get_vraw_image() if self._external_frame_source is None else self._external_frame_source()
                render = time.perf_counter()
                if USE_MICRO:
                    self.disp.show()
                else:
                    self.disp.display()
                if config.SHOW_STATS:
                    self._inc_frame(enter, start, render, time.perf_counter())

    def get_vraw_image(self):
        return self.pilimg.tobytes(encoder_name="vraw")

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
            # Extract pixels as vraw
            pil_buf = self.get_vraw_image() if self._external_frame_source is None else self._external_frame_source()
            # Create a linear buffer to hold expanded pyglet-L pixels
            lin_buf = [0 for i in range(len(pil_buf) * 8)]
            BITS = [0, 1, 2, 3, 4, 5, 6, 7]
            # Transform V-packed pixels to linear buffer
            for i in range(len(pil_buf)):
                x = i % config.WIDTH
                page = (i // config.WIDTH) * 8
                mask = 0x01
                for b in BITS:
                    y = page + b
                    lin_buf[(y * config.WIDTH) + x] = 255 if pil_buf[i] & mask else 0
                    mask <<= 1
            # Make it a byte-string
            frame = pack(f">{len(lin_buf)}B", *lin_buf)
            # Create a pyglet image from it
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
            pyglet.clock.schedule(OledDisplay.update_image)
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
