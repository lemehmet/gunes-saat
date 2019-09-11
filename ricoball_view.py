import math
import random
import config
from common import log_paint, log_fw
from views import View

PI = math.pi
IKIPI = 2 * PI


def _normalize(angle):
    if angle > 0.0:
        if angle > PI:
            angle = angle - (math.ceil(angle / (IKIPI)) * IKIPI)
    else:
        if angle < -PI:
            angle = angle + (math.ceil(angle / (IKIPI)) * IKIPI)
    return angle

class RicoBall(View):
    x = 0
    y = 0
    r = 4
    v = 0.0
    a = 0.0
    filled = True

    def __init__(self, display):
        View.__init__(self, display)
        random.seed()
        self._randomize()

    def _randomize(self):
        self.x = random.randrange(0, config.WIDTH + 1)
        self.y = random.randrange(0, config.HEIGHT + 1)
        self.v = random.random() * 10.0
        self.a = (random.random() - 0.5) * IKIPI

    def _move_ball(self):
        dx = math.ceil(self.v * math.cos(self.a))
        dy = math.ceil(self.v * math.sin(self.a))
        if self.x + dx >= config.WIDTH or self.x + dx <= 0:
            dx = -dx
            self.a = _normalize(PI - self.a)
        if self.y + dy >= config.HEIGHT or self.y + dy <= 0:
            dy = -dy
            self.a = _normalize(-self.a)
        self.x += dx
        self.y += dy

    def paint(self):
        log_paint.debug(f"RicoBall::paint() {self.x} x {self.y} {self.a} {self.v}")
        with self.display.mutex_disp:
            bounds = ((self.x - self.r, self.y - self.r), (self.x + self.r, self.y + self.r))
            self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
            self.display.draw.ellipse(bounds, fill=config.FG if self.filled else None, outline=config.FG, width=1)

    def on_sched_event(self):
        log_fw.debug("RicoBall::on_sched_event()")
        self._move_ball()
        self.paint()

    def on_button_a(self, pressed, repeated):
        # Re-randomize the initial position, direction and speed
        if pressed and not repeated:
            self._randomize()
        self.paint()

    def on_button_b(self, pressed, repeated):
        # Toggle filled/empty ball
        if pressed and not repeated:
            self.filled = not self.filled
            self.paint()

    def on_button_c(self, pressed, repeated):
        # Do nothing
        pass

    def on_button_up(self, pressed, repeated):
        # Increase the size of the ball
        if pressed:
            self.r = self.r + 1 if self.y < self.display.my else self.display.my
        self.paint()

    def on_button_down(self, pressed, repeated):
        # Decrease the size of the ball
        if pressed:
            self.r = self.r - 1 if self.y > 1 else 1
        self.paint()

    def on_button_left(self, pressed, repeated):
        # Change the direction by 15 degrees to ccw
        if pressed and not repeated:
            self.a = _normalize(self.a + (PI / 12.0))
        self.paint()

    def on_button_right(self, pressed, repeated):
        # Change the direction by 15 degrees to cw
        if pressed and not repeated:
            self.a = _normalize(self.a - (PI / 12.0))
        self.paint()
