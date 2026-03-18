# logic.py
from PySide6.QtCore import QObject, Signal

class CounterLogic(QObject):
    value_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._count = 0

    def oni(self):
        self._count +=1
        self.value_changed.emit(self._count)

    def onr(self):
        self._count = 0
        self.value_changed.emit(0)
