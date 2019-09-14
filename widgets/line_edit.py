
from PyQt5.QtWidgets import QLineEdit

class LineEdit(QLineEdit):
    def __init__(self, parent, row=0, col=0, row_span=0, col_span=0):
        super().__init__()
        self.row = row
        self.col = col
        self.row_span = row_span
        self.col_span = col_span
