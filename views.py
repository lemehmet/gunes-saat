from math import floor
from time import strftime, localtime

from PIL import ImageFont

import config


class View:
    left = None
    right = None
    up = None
    down = None

    def __init__(self, display):
        self.display = display

    def set_left(self, view):
        prev = self.left
        self.left = view
        return prev

    def set_right(self, view):
        prev = self.right
        self.right = view
        return prev

    def set_up(self, view):
        prev = self.up
        self.up = view
        return prev

    def set_down(self, view):
        prev = self.down
        self.down = view
        return prev

    def activate(self):
        pass

    def paint(self):
        pass

    def on_sched_event(self):
        pass

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


class Manager:
    def __init__(self, root):
        self.root = root
        self._set_current(self.root)

    def _set_current(self, view):
        self.current = view
        self.paint = self.current.paint
        self.activate = self.current.activate
        self.on_sched_event = self.current.on_sched_event
        self.on_button_a = self.current.on_button_a
        self.on_button_b = self.current.on_button_b
        self.on_button_c = self.current.on_button_c
        self.on_button_left = self.current.on_button_left
        self.on_button_right = self.current.on_button_right
        self.on_button_up = self.current.on_button_up
        self.on_button_down = self.current.on_button_down
        self.activate()

    def _move(self, target):
        prev = self.current
        if target != None:
            self._set_current(target)
        return prev

    def move_right(self):
        return self._move(self.current.right)

    def move_left(self):
        return self._move(self.current.left)

    def move_up(self):
        return self._move(self.current.up)

    def move_down(self):
        return self._move(self.current.down)


class ClockView(View):
    blink_state = False
    font_index = 3

    def __init__(self, display):
        View.__init__(self, display)
        self._set_clock_font()

    def activate(self):
        pass

    def paint(self):
        # Background
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
        # Clock
        self.blink_state = not self.blink_state
        clock_text = strftime(f"%I{':' if self.blink_state else '.'}%M %p", localtime())
        text_width, text_height = self.display.draw.textsize(clock_text, font=self.font)
        self.display.draw.text((self.display.cx - text_width // 2, self.display.cy - text_height // 2), clock_text, font=self.font, fill=config.FG)


    def _set_clock_font(self):
        print(f"Setting font {config.FONTS[self.font_index][0]} x{config.FONTS[self.font_index][1]}")
        try:
            self.font = ImageFont.truetype(f"./fonts/{config.FONTS[self.font_index][0]}",
                                           floor(config.CLOCK_FONT_SIZE * config.FONTS[self.font_index][1]))
        except OSError as err:
            print(f"Error while opening font: {err.filename}, {err.filename2}: {err.strerror} {err.errno}")


    def on_sched_event(self):
        self.paint()

    def on_button_a(self, pressed):
        if pressed:
            self.font_index = self.font_index + 1 if (self.font_index + 1) < len(config.FONTS) else 0
            self._set_clock_font()
            self.display.update_image()

    def on_button_b(self, pressed):
        if pressed:
            self.font_index = self.font_index - 1 if self.font_index > 0 else len(config.FONTS) - 1
            self._set_clock_font()
            self.display.update_image()

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


class MovingBall(View):
    radius = 10
    x = radius
    y = radius

    def __init__(self, display):
        View.__init__(self, display)

    def activate(self):
        pass

    def paint(self):
        # Background
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
        self.display.draw.ellipse(((self.x - self.radius, self.y - self.radius),
                                   (self.x + self.radius, self.y + self.radius)), fill=config.FG, width=self.radius)


    def on_sched_event(self):
        self.paint()

    def on_button_a(self, pressed):
        if pressed:
            self.radius = self.radius - 1 if self.radius > 1 else self.radius
        self.paint()

    def on_button_b(self, pressed):
        if pressed:
            self.radius = self.radius + 1 if self.radius < self.display.my else self.radius
        self.paint()

    def on_button_c(self, pressed):
        pass

    def on_button_up(self, pressed):
        if pressed:
            self.y = self.y - 1 if self.y > 1 else self.y
        self.paint()

    def on_button_down(self, pressed):
        if pressed:
            self.y = self.y + 1 if self.y < self.display.my else self.y
        self.paint()

    def on_button_left(self, pressed):
        if pressed:
            self.x = self.x - 1 if self.x > 1 else self.x
        self.paint()

    def on_button_right(self, pressed):
        if pressed:
            self.x = self.x + 1 if self.x < self.display.mx else self.x
        self.paint()
