from PyQt5.QtWidgets import QGridLayout

class GridLayout(QGridLayout):
    def __init__(self, parent):
        super().__init__()
        
    def add_widget(self, widget):
        if widget.row_span or widget.col_span:
            self.addWidget(widget, widget.row, widget.col, widget.row_span, widget.col_span)
            return
        self.addWidget(widget, widget.row, widget.col)

    def add_widgets(self, *widgets):
        for widget in widgets:
            self.add_widget(widget)
            
    def add_layout(self, layout):
        if layout.row_span or layout.col_span:
            self.addLayout(layout, layout.row, layout.col, layout.row_span, layout.col_span)
        else:
            self.addLayout(layout, layout.row, layout.col)

    