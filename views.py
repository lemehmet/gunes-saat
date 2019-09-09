from enum import Enum, unique

import config
from common import log_paint, log_fw
from display import dump_pilbuffer


class View:
    left = None
    right = None
    up = None
    down = None

    def __init__(self, display):
        self.display = display

    def paint(self):
        log_paint.debug("View::paint()")
        self.display.paint()

    def set_left(self, view):
        prev = self.left
        self.left = view
        return prev

    def set_right(self, view):
        prev = self.right
        self.right = view
        return prev

    def set_up(self, view):
        prev = self.up
        self.up = view
        return prev

    def set_down(self, view):
        prev = self.down
        self.down = view
        return prev

    def activate(self):
        pass

    def on_sched_event(self):
        log_fw.debug("View::on_sched_event()")

    def on_button_a(self, pressed, repeated):
        pass

    def on_button_b(self, pressed, repeated):
        pass

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


@unique
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Manager:
    _pressed_button = None
    _selecting_view = False
    _sliding_direction = None
    _sliding_step = 0
    _slider_buffer = None
    _prev_image = None
    _next_image = None

    def __init__(self, root):
        self.root = root
        self._set_current(self.root)

    def _set_current(self, view):
        self.current = view
        self._paint = self.current.paint
        self.activate = self.current.activate
        self._on_sched_event = self.current.on_sched_event
        self._on_button_a = self.current.on_button_a
        self._on_button_b = self.current.on_button_b
        self._on_button_c = self.current.on_button_c
        self._on_button_left = self.current.on_button_left
        self._on_button_right = self.current.on_button_right
        self._on_button_up = self.current.on_button_up
        self._on_button_down = self.current.on_button_down
        self.activate()

    def paint(self):
        log_paint.debug("Manager::paint()")
        self._paint()

    def on_sched_event(self):
        if self._pressed_button is not None:
            self._pressed_button(True, True)
        elif self._sliding_direction is not None:
            # TODO: Do the animation here
            pass
        self._on_sched_event()

    def _handle_repeat(self, pressed, handler):
        self._pressed_button = handler if pressed else None

    def on_button_a(self, pressed):
        self._handle_repeat(pressed, self._on_button_a)
        self._on_button_a(pressed, False)

    def on_button_b(self, pressed):
        self._handle_repeat(pressed, self._on_button_b)
        self._on_button_b(pressed, False)

    def on_button_c(self, pressed):
        if pressed:
            self._selecting_view = not self._selecting_view
            log_fw.info(f"{'Selecting view' if self._selecting_view else 'Done view selection'}")

    def on_button_up(self, pressed):
        if pressed and self._selecting_view:
            self.move_up()
        else:
            self._handle_repeat(pressed, self._on_button_up)
            self._on_button_up(pressed, False)

    def on_button_down(self, pressed):
        if pressed and self._selecting_view:
            self.move_down()
        else:
            self._handle_repeat(pressed, self._on_button_down)
            self._on_button_down(pressed, False)

    def on_button_left(self, pressed):
        if pressed and self._selecting_view:
            self.move_left()
        else:
            self._handle_repeat(pressed, self._on_button_left)
            self._on_button_left(pressed, False)

    def on_button_right(self, pressed):
        if pressed and self._selecting_view:
            self.move_right()
        else:
            self._handle_repeat(pressed, self._on_button_right)
            self._on_button_right(pressed, False)

    def render_sliding_view(self):
        if self._sliding_direction is None:
            # This shouldn't happen
            raise RuntimeError("Sliding renderer cannot render when not sliding")
        elif self._sliding_direction == Direction.UP:
            pass
        elif self._sliding_direction == Direction.DOWN:
            pass
        elif self._sliding_direction == Direction.LEFT:
            self.hslide(config.WIDTH - ((config.WIDTH // config.HSLIDING_STEPS) * self._sliding_step), self._prev_image, self._next_image)
        elif self._sliding_direction == Direction.RIGHT:
            self.hslide((config.WIDTH // config.HSLIDING_STEPS) * self._sliding_step, self._next_image, self._prev_image)
        self._sliding_step += 1
        if self._sliding_step >= config.HSLIDING_STEPS:
            self._sliding_direction = None
            self.current.display.set_external_framer(None)
        return self._slider_buffer

    def hslide(self, sep, a, b):
        pages = config.HEIGHT // 8
        index = 0
        for page in range(pages):
            offset = page * config.WIDTH
            for x in range(0, sep):
                self._slider_buffer[index] = a[offset + x]
                index += 1
            for x in range(sep, config.WIDTH):
                self._slider_buffer[index] = b[offset + x]
                index += 1

    def _move(self, target, direction):
        prev = self.current
        if target is not None:
            self._sliding_direction = direction
            self._sliding_step = 0
            # Make sure display returns its real image buffer
            self.current.display.set_external_framer(None)
            self.paint()
            self._prev_image = self.current.display.get_vraw_image()
            self._set_current(target)
            self.paint()
            self._next_image = self.current.display.get_vraw_image()
            self._slider_buffer = []
            self._slider_buffer[:] = self._prev_image[:]
            # Store image buffers of previous and nexy views and set display to invoke manager's frame buffer source when painting
            self.current.display.set_external_framer(self.render_sliding_view)
        return prev

    def move_right(self):
        return self._move(self.current.right, Direction.RIGHT)

    def move_left(self):
        return self._move(self.current.left, Direction.LEFT)

    def move_up(self):
        return self._move(self.current.up, Direction.UP)

    def move_down(self):
        return self._move(self.current.down, Direction.DOWN)
