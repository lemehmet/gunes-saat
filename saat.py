from math import floor
from time import localtime, strftime

from PIL import ImageFont

import config
import display

class Saat(display.OledDisplay):
    test_pixel = [120, 60]
    font_index = 0
    mx = config.WIDTH - 1
    my = config.HEIGHT - 2
    cx = config.WIDTH // 2
    cy = config.HEIGHT // 2
    the_dot = False

    def __init__(self):
        display.OledDisplay.__init__(self)
        print(f"Doing saat init. {self.draw}")
        self.set_clock_font()
        self.wp_update()

    def wp_background(self):
        self.draw.rectangle((0, 0, self.mx, self.my), fill=config.BG, outline=config.FG)
        # self.draw.polygon(
        #     ((1, 1),
        #     (config.WIDTH - 1, 1),
        #     (config.WIDTH - 1, config.HEIGHT - 1),
        #     (1, config.HEIGHT - 1)), outline=0
        # )

    def clock_now(self):
        self.the_dot = not self.the_dot
        return strftime(f"%I{':' if self.the_dot else '.'}%M %p", localtime())

    def wp_debug(self):
        print(f"Font: {self.font.getname()} Pixel: ({self.test_pixel[0], self.test_pixel[1]})")
        self.draw.point((self.test_pixel[0], self.test_pixel[1]), fill=config.FG)


    def wp_clock(self):
        now = self.clock_now()
        print(f"{now}")
        text_width, text_height = self.draw.textsize(now, font=self.font)
        self.draw.text((self.cx - text_width // 2, self.cy - text_height // 2), now, font=self.font, fill=config.FG)

    def wp_update(self):
        self.wp_background()
        self.wp_debug()
        self.wp_clock()
        self.update()

    def set_clock_font(self):
        self.font = ImageFont.truetype(f"./fonts/{config.FONTS[self.font_index][0]}",
                                       floor(config.CLOCK_FONT_SIZE * config.FONTS[self.font_index][1]))

    def on_half_second(self):
        self.wp_update()
        display.OledDisplay.on_half_second(self)

    def on_button_a(self, pressed):
        if pressed:
            self.font_index = self.font_index + 1 if (self.font_index + 1) < len(config.FONTS) else 0
            self.set_clock_font()
            self.wp_update()

    def on_button_b(self, pressed):
        if pressed:
            self.font_index = self.font_index - 1 if self.font_index > 0 else len(config.FONTS) - 1
            self.set_clock_font()
            self.wp_update()

    def on_button_c(self, pressed):
        print(f"Saat::C(pressed={pressed})")


    def on_button_up(self, pressed):
        if pressed:
            self.test_pixel[1] -= 1
            self.wp_update()


    def on_button_down(self, pressed):
        if pressed:
            self.test_pixel[1] += 1
            self.wp_update()


    def on_button_left(self, pressed):
        if pressed:
            self.test_pixel[0] -= 1
            self.wp_update()


    def on_button_right(self, pressed):
        if pressed:
            self.test_pixel[0] += 1
            self.wp_update()



if __name__ == '__main__':
    saat = Saat()
    saat.run()



