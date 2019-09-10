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
        diag_lines = DiagnosticLine(display=self)
        rico_ball = RicoBall(display=self)
        tv_center = TextView(display=self, text="Center")
        tv_n = TextView(display=self, text="N")
        tv_s = TextView(display=self, text="S")
        tv_e = TextView(display=self, text="E")
        tv_w = TextView(display=self, text="W")
        tv_nw = TextView(display=self, text="NW")
        tv_ne = TextView(display=self, text="NE")
        tv_sw = TextView(display=self, text="SW")
        tv_se = TextView(display=self, text="SE")
        # Full compass
        tv_center.set_up(tv_n)
        tv_center.set_down(tv_s)
        tv_center.set_left(tv_w)
        tv_center.set_right(tv_e)
        tv_n.set_down(tv_center)
        tv_n.set_left(tv_nw)
        tv_n.set_right(tv_ne)
        tv_s.set_up(tv_center)
        tv_s.set_left(tv_sw)
        tv_s.set_right(tv_se)
        tv_w.set_right(tv_center)
        tv_w.set_up(tv_nw)
        tv_w.set_down(tv_sw)
        tv_e.set_left(tv_center)
        tv_e.set_up(tv_ne)
        tv_e.set_down(tv_se)
        tv_nw.set_right(tv_n)
        tv_nw.set_down(tv_w)
        tv_ne.set_left(tv_n)
        tv_ne.set_down(tv_e)
        tv_sw.set_up(tv_w)
        tv_sw.set_right(tv_s)
        tv_se.set_up(tv_e)
        tv_se.set_left(tv_s)
        # Roll over to normal functions from east and west
        tv_e.set_right(rico_ball)
        tv_w.set_left(clock_view)

        rico_ball.set_left(tv_e)
        rico_ball.set_right(diag_lines)
        diag_lines.set_left(rico_ball)
        diag_lines.set_right(clock_view)
        clock_view.set_left(diag_lines)
        clock_view.set_right(moving_ball)
        moving_ball.set_left(clock_view)
        moving_ball.set_right(tv_w)

        self.vm = Manager(tv_center)
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
