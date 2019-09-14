from PyQt5.QtWidgets import QHBoxLayout

class HorizontalLayout(QHBoxLayout):
    def __init__(self, row=0, col=0, row_span=0, col_span=0):
        super().__init__()
        self.row = row
        self.col = col
        self.row_span = row_span
        self.col_span = col_span

    def add_elements(self, *widgets):
        for widget in widgets:
            self.addWidget(widget)