import threading


class AtomicValue:
    def __init__(self, initial):
        self._value = initial
        self._lock = threading.Lock()

    def set(self, value):
        with self._lock:
            v = self._value
            self._value = value
            return v

    def get(self):
        with self._lock:
            return self._value