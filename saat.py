from math import floor
from time import localtime, strftime

from PIL import ImageFont

import config
import display
from views import Manager, ClockView


class Saat(display.OledDisplay):
    mx = config.WIDTH - 1
    my = config.HEIGHT - 2
    cx = config.WIDTH // 2
    cy = config.HEIGHT // 2

    def __init__(self):
        display.OledDisplay.__init__(self)
        clock_view = ClockView(display=self)
        self.vm = Manager(clock_view)
        # TODO: Invoke the current view's initialize
        self.vm.paint()


    def on_sched_event(self):
        try:
            display.OledDisplay.on_sched_event(self)
            self.vm.on_sched_event()
        except AttributeError:
            print("Too early to receive scheduler events, will try again")

    def on_button_a(self, pressed):
            self.vm.on_button_a(pressed)

    def on_button_b(self, pressed):
            self.vm.on_button_b(pressed)

    def on_button_c(self, pressed):
        self.vm.on_button_c(pressed)

    def on_button_up(self, pressed):
        self.vm.on_button_up(pressed)


    def on_button_down(self, pressed):
        self.vm.on_button_down(pressed)


    def on_button_left(self, pressed):
        self.vm.on_button_left(pressed)


    def on_button_right(self, pressed):
        self.vm.on_button_right(pressed)



if __name__ == '__main__':
    saat = Saat()
    saat.run()



