from enum import Enum, unique

from common import log_paint, log_fw


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
    _scroll_direction = None

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
        elif self._scroll_direction is not None:
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
        # self._handle_repeat(pressed, self._on_button_c)
        # self._on_button_c(pressed, False)

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

    def _move(self, target, direction):
        prev = self.current
        if target is not None:
            self._scroll_direction = direction
            self._set_current(target)
        return prev

    def move_right(self):
        return self._move(self.current.right, Direction.RIGHT)

    def move_left(self):
        return self._move(self.current.left, Direction.LEFT)

    def move_up(self):
        return self._move(self.current.up, Direction.UP)

    def move_down(self):
        return self._move(self.current.down, Direction.DOWN)
