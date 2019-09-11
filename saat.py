import config
import display
from clock_view import ClockView
from common import log_paint, log_fw
from diag_lines import DiagnosticLine
from moving_ball_view import MovingBall
from ricoball_view import RicoBall
from text_view import TextView
from views import Manager


class Saat(display.OledDisplay):
    mx = config.WIDTH - 1
    my = config.HEIGHT - 1
    cx = config.WIDTH // 2
    cy = config.HEIGHT // 2

    def __init__(self):
        log_fw.debug("Initializing")
        display.OledDisplay.__init__(self)
        clock_view = ClockView(display=self)
        moving_ball = MovingBall(display=self)
        rico_ball = RicoBall(display=self)

        rico_ball.set_right(clock_view)
        clock_view.set_left(rico_ball)
        clock_view.set_right(moving_ball)
        moving_ball.set_left(clock_view)
        moving_ball.set_right(rico_ball)

        self.vm.set_root_view(rico_ball)
        # TODO: Invoke the current view's initialize
        self.vm.paint()
        log_fw.debug("Issued initial paint")

    def paint(self):
        log_paint.debug("Saat::paint()")

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
