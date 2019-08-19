from math import floor
from time import localtime, strftime

from PIL import ImageFont

import config
import display
from common import log_paint, log_fw
from views import Manager, ClockView, MovingBall


class Saat(display.OledDisplay):
    mx = config.WIDTH - 1
    my = config.HEIGHT - 2
    cx = config.WIDTH // 2
    cy = config.HEIGHT // 2
    selecting_view = False

    def __init__(self):
        log_fw.debug("Initializing")
        display.OledDisplay.__init__(self)
        clock_view = ClockView(display=self)
        moving_ball = MovingBall(display=self)
        clock_view.set_right(moving_ball)
        moving_ball.set_left(clock_view)
        self.vm = Manager(clock_view)
        # TODO: Invoke the current view's initialize
        self.vm.paint()
        log_fw.debug("Issued initial paint")

    def paint(self):
        log_paint.debug("Saat::paint()")

    def on_sched_event(self):
        try:
            display.OledDisplay.on_sched_event(self)
            self.vm.on_sched_event()
            self.update_image()
        except AttributeError:
            log_fw.warning("Too early to receive scheduler events, will try again")

    def on_button_a(self, pressed):
        self.vm.on_button_a(pressed)

    def on_button_b(self, pressed):
        self.vm.on_button_b(pressed)

    def on_button_c(self, pressed):
        if pressed:
            self.selecting_view = not self.selecting_view
            log_fw.info(f"{'Selecting view' if self.selecting_view else 'Done view selection'}")
        # self.vm.on_button_c(pressed)

    def on_button_up(self, pressed):
        self.vm.on_button_up(pressed)

    def on_button_down(self, pressed):
        self.vm.on_button_down(pressed)

    def on_button_left(self, pressed):
        if self.selecting_view:
            self.vm.move_left()
        self.vm.on_button_left(pressed)

    def on_button_right(self, pressed):
        if self.selecting_view:
            self.vm.move_right()
        self.vm.on_button_right(pressed)


if __name__ == '__main__':
    saat = Saat()
    saat.run()
