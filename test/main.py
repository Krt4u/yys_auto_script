# main.py (组装器)
from PySide6.QtWidgets import QApplication
from view import CounterView
from logic import CounterLogic

app = QApplication([])

view = CounterView()
logic = CounterLogic()

view.ir.connect(logic.oni)
view.rr.connect(logic.onr)

logic.value_changed.connect(view.update_display)

view.show()

app.exec()