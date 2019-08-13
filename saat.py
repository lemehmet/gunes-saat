import config
import display

class Saat(display.OledDisplay):
    test_pixel = [120, 60]

    def __init__(self):
        display.OledDisplay.__init__(self)
        print(f"Doing saat init. {self.draw}")
        self.wp_background()

    def wp_background(self):
        self.draw.rectangle((0, 0, config.WIDTH, config.HEIGHT), fill=config.BG)
        # self.draw.polygon(
        #     ((1, 1),
        #     (config.WIDTH - 1, 1),
        #     (config.WIDTH - 1, config.HEIGHT - 1),
        #     (1, config.HEIGHT - 1)), outline=0
        # )

    def wp_debug(self):
        print(f"Pixel: ({self.test_pixel[0], self.test_pixel[1]})")
        self.draw.point((self.test_pixel[0], self.test_pixel[1]), fill=config.FG)

    def wp_update(self):
        self.wp_background()
        self.wp_debug()
        self.update()

    def on_button_a(self, pressed):
        print(f"Saat::A(pressed={pressed})")

    def on_button_b(self, pressed):
        print(f"Saat::B(pressed={pressed})")


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



