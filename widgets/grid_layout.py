from PyQt5.QtWidgets import QGridLayout

class GridLayout(QGridLayout):
    def __init__(self, parent):
        super().__init__()
        
    def add_widget(self, widget):
        if widget.row_span and widget.col_span:
            self.addWidget(widget, widget.row, widget.col, widget.row_span, widget.col_span)
            return
        self.addWidget(widget, widget.row, widget.col)