from math import floor
from datetime import datetime
from PIL import ImageFont

import config
from common import log_paint, log_fw
from views import View


class ClockView(View):
    last_clock_text = ""
    font_index = 3

    def __init__(self, display):
        View.__init__(self, display)
        self._set_clock_font()

    def activate(self):
        pass

    @staticmethod
    def _clock_text():
        now = datetime.now()
        return now.strftime(f"%I{':' if now.microsecond < 500000 else '.'}%M %p")

    def paint(self):
        log_paint.debug("ClockView::paint()")
        # Background
        self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
        # Clock
        clock_text = self._clock_text()
        text_width, text_height = self.display.draw.textsize(clock_text, font=self.font)
        self.display.draw.text((self.display.cx - text_width // 2, self.display.cy - text_height // 2), clock_text, font=self.font, fill=config.FG)
        View.paint(self)
        self.last_clock_text = clock_text

    def _set_clock_font(self):
        log_fw.debug(f"Setting font {config.FONTS[self.font_index][0]} x{config.FONTS[self.font_index][1]}")
        try:
            self.font = ImageFont.truetype(f"./fonts/{config.FONTS[self.font_index][0]}", floor(config.CLOCK_FONT_SIZE * config.FONTS[self.font_index][1]))
        except OSError as err:
            log_fw.exception(f"Error while opening font: {err.filename}, {err.filename2}: {err.strerror} {err.errno}")

    def on_sched_event(self):
        log_fw.debug("ClockView::on_sched_event()")
        clock_text = self._clock_text()
        if clock_text != self.last_clock_text:
            self.paint()

    def on_button_a(self, pressed, repeated):
        if pressed:
            self.font_index = self.font_index + 1 if (self.font_index + 1) < len(config.FONTS) else 0
            self._set_clock_font()
            self.display.update_image()

    def on_button_b(self, pressed, repeated):
        if pressed:
            self.font_index = self.font_index - 1 if self.font_index > 0 else len(config.FONTS) - 1
            self._set_clock_font()
            self.display.update_image()

    def on_button_c(self, pressed, repeated):
        pass

    def on_button_up(self, pressed, repeated):
        pass

    def on_button_down(self, pressed, repeated):
        pass

    def on_button_left(self, pressed, repeated):
        pass

    def on_button_right(self, pressed, repeated):
        pass

