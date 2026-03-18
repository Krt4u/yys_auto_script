# view.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class CounterView(QWidget):

    ir = Signal()
    rr = Signal()

    def __init__(self):
        super().__init__()
        self.setGeometry(300,300,300,300)

        self.init_ui()

    def init_ui(self):
        self.label = QLabel("0")
        self.btn_inc = QPushButton("增加")
        self.btn_reset = QPushButton("重置")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_inc)
        layout.addWidget(self.btn_reset)

        self.btn_inc.clicked.connect(self.ir.emit)
        self.btn_reset.clicked.connect(self.rr.emit)

    def update_display(self, value):
        self.label.setText((str(value)))

        