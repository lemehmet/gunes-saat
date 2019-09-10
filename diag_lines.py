from math import floor

from PIL import ImageFont

import config
from common import log_paint, log_fw
from views import View


class DiagnosticLine(View):
    len = config.WIDTH
    x = 0
    y = config.HEIGHT // 2

    def __init__(self, display):
        View.__init__(self, display)

    def activate(self):
        pass

    def paint(self):
        log_paint.debug(f"DiagnosticLine::paint() {self.x} x {self.y} {self.len}")
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.BG)
        self.display.draw.line(((self.x, self.y), (self.x + self.len, self.y)), fill=config.FG)

    def on_sched_event(self):
        log_fw.debug("DiagnosticLine::on_sched_event()")
        self.paint()

    def on_button_a(self, pressed, repeated):
        if pressed:
            self.len = self.len - 1 if self.len > 1 else self.len
        self.paint()

    def on_button_b(self, pressed, repeated):
        if pressed:
            self.len = self.len + 1 if self.len < self.display.mx else self.len
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
