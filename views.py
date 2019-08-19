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


class Manager:
    _pressed_button = None

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
        self._handle_repeat(pressed, self._on_button_c)
        self._on_button_c(pressed, False)

    def on_button_up(self, pressed):
        self._handle_repeat(pressed, self._on_button_up)
        self._on_button_up(pressed, False)

    def on_button_down(self, pressed):
        self._handle_repeat(pressed, self._on_button_down)
        self._on_button_down(pressed, False)

    def on_button_left(self, pressed):
        self._handle_repeat(pressed, self._on_button_left)
        self._on_button_left(pressed, False)

    def on_button_right(self, pressed):
        self._handle_repeat(pressed, self._on_button_right)
        self._on_button_right(pressed, False)

    def _move(self, target):
        prev = self.current
        if target is not None:
            self._set_current(target)
        return prev

    def move_right(self):
        return self._move(self.current.right)

    def move_left(self):
        return self._move(self.current.left)

    def move_up(self):
        return self._move(self.current.up)

    def move_down(self):
        return self._move(self.current.down)
