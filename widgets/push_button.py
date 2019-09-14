from PyQt5.QtWidgets import QPushButton

class PushButton(QPushButton):
    def __init__(self, label, parent, row=0, col=0, row_span=0, col_span=0, click_slot="", press_slot=""):
        super().__init__()
        if click_slot:
            self.clicked.connect(click_slot)
        
        if press_slot:
            self.pressed.connect(press_slot)
        self.setText(label)
        self.row = row
        self.col = col
        self.row_span = row_span
        self.col_span = col_span

    def hide(self):
        self.setGeometry()