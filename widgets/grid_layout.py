from PyQt5.QtWidgets import QGridLayout

class GridLayout(QGridLayout):
    def __init__(self, parent):
        self.layout = GridLayout(parent)

    def add_widget(self, widget):
        self.layout.addWidget(widget, widget.row, widget.col, widget.row_span, widget.col_span)
