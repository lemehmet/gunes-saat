from math import floor

from PIL import ImageFont

import config
from common import log_paint, log_fw
from views import View


class MovingBall(View):
    radius = 10
    x = radius
    y = radius

    def __init__(self, display):
        View.__init__(self, display)
        self.font = ImageFont.truetype(f"./fonts/{config.FONTS[3][0]}", floor(8 * config.FONTS[3][1]))

    def activate(self):
        pass

    def paint(self):
        log_paint.debug("MovingBall::paint()")
        # Background
        bounds = ((self.x - self.radius, self.y - self.radius), (self.x + self.radius, self.y + self.radius))
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
        self.display.draw.ellipse(bounds, fill=config.FG, width=self.radius)
        self.display.draw.rectangle(bounds, outline=config.FG)
        self.display.draw.line(((self.x, self.y - self.radius), (self.x, self.y + self.radius)), fill=config.BG)
        self.display.draw.line(((self.x - self.radius, self.y), (self.x + self.radius, self.y)), fill=config.BG)
        crtext = f"[{self.x},{self.y}]"
        cx, cy = self.display.draw.textsize(crtext, font=self.font)
        self.display.draw.text((0, 0), crtext, font=self.font, fill=config.FG)
        self.display.draw.text((0, cy + 1), crtext, font=self.font, fill=config.BG)
        self.display.draw.text((self.display.mx - cx, 0), crtext, font=self.font, fill=config.FG)
        self.display.draw.text((self.display.mx - cx, cy + 1), crtext, font=self.font, fill=config.BG)
        self.display.draw.text((0, self.display.my - 2 * cy - 2), crtext, font=self.font, fill=config.FG)
        self.display.draw.text((0, self.display.my - cy - 1), crtext, font=self.font, fill=config.BG)
        self.display.draw.text((self.display.mx - cx, self.display.my - 2 * cy - 2), crtext, font=self.font, fill=config.FG)
        self.display.draw.text((self.display.mx - cx, self.display.my - cy - 1), crtext, font=self.font, fill=config.BG)


    def on_sched_event(self):
        log_fw.debug("MovingBall::on_sched_event()")
        self.paint()

    def on_button_a(self, pressed, repeated):
        if pressed:
            self.radius = self.radius - 1 if self.radius > 1 else self.radius
        self.paint()

    def on_button_b(self, pressed, repeated):
        if pressed:
            self.radius = self.radius + 1 if self.radius < self.display.my else self.radius
        self.paint()

    def on_button_c(self, pressed, repeated):
        pass

    def on_button_up(self, pressed, repeated):
        if pressed:
            self.y = self.y - 1 if self.y > 0 else self.y
        self.paint()

    def on_button_down(self, pressed, repeated):
        if pressed:
            self.y = self.y + 1 if self.y < self.display.my else self.y
        self.paint()

    def on_button_left(self, pressed, repeated):
        if pressed:
            self.x = self.x - 1 if self.x > 0 else self.x
        self.paint()

    def on_button_right(self, pressed, repeated):
        if pressed:
            self.x = self.x + 1 if self.x < self.display.mx else self.x
        self.paint()
