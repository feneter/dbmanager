from PyQt5.QtWidgets import QPushButton

class PushButton(QPushButton):
    def __init__(self, label, parent, row=0, col=0, row_span=0, col_span=0, click_slot="", press_slot=""):
        self.button = QPushButton(label, parent)
        if click_slot:
            self.button.clicked.connect(click_slot)
        
        if press_slot:
            self.button.pressed.connect(press_slot)
        self.row = row
        self.col = col
        self.row_span = row_span
        self.col_span = col_span
