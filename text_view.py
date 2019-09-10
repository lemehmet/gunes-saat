from math import floor

from PIL import ImageFont

import config
from common import log_paint, log_fw, log_view
from views import View


class TextView(View):
    text = "Gunes'in Saati"
    font = None
    x = config.WIDTH // 2
    y = config.HEIGHT // 2
    tx = 0
    ty = 0

    def __init__(self, display, text, font_index=7, size=config.CLOCK_FONT_SIZE):
        View.__init__(self, display)
        self.text = text
        self.size = size
        self.font_path = f"./fonts/{config.FONTS[font_index][0]}"
        self._create_font()

    def __repr__(self):
        return f"TV:'{self.text}'@{self.x}x{self.y} of size {self.size}"

    def _create_font(self):
        self.font = ImageFont.truetype(self.font_path, self.size)
        log_view.info(f"TV: Setting font, size: {self.size} of {self.font_path}")
        self._update_dims()

    def _update_dims(self):
        # Text method uses top-left corner as xy coordinate
        cx, cy = self.display.draw.textsize(self.text, font=self.font)
        self.tx = self.x - (cx // 2)
        self.ty = self.y - (cy // 2)
        log_view.info(f"TV: Setting dims, size: {cx}x{cy} top-left: {self.tx}x{self.ty}")

    def activate(self):
        pass

    def paint(self):
        log_paint.debug(f"TextView::paint() {self.x} x {self.y} {self.size}")
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.BG)
        self.display.draw.text((self.tx, self.ty), self.text, font=self.font, fill=config.FG)

    def on_sched_event(self):
        log_fw.debug("TextView::on_sched_event()")
        self.paint()

    def on_button_a(self, pressed, repeated):
        if pressed and not repeated:
            self.size -= 1
            self._create_font()
        self.paint()

    def on_button_b(self, pressed, repeated):
        if pressed and not repeated:
            self.size += 1
            self._create_font()
        self.paint()

    def on_button_c(self, pressed, repeated):
        pass

    def on_button_up(self, pressed, repeated):
        if pressed:
            self.y = self.y - 1 if self.y > 0 else self.y
            self._update_dims()
        self.paint()

    def on_button_down(self, pressed, repeated):
        if pressed:
            self.y = self.y + 1 if self.y < self.display.my else self.y
            self._update_dims()
        self.paint()

    def on_button_left(self, pressed, repeated):
        if pressed:
            self.x = self.x - 1 if self.x > 0 else self.x
            self._update_dims()
        self.paint()

    def on_button_right(self, pressed, repeated):
        if pressed:
            self.x = self.x + 1 if self.x < self.display.mx else self.x
            self._update_dims()
        self.paint()
