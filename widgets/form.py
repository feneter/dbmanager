from PyQt5.QtWidgets import QWidget

from widgets.line_edit import LineEdit
from widgets.push_button import PushButton
from widgets.grid_layout import GridLayout

class Form(QWidget):
    def __init__(self, parent, show_primary_buttons=False):
        super().__init__()
        self.setParent(parent)
        self.next_row = 0
        self.layout = GridLayout(self)
        self.show_buttons = show_primary_buttons
        self.clear_button = PushButton("Clear", self, row=0, col=0)
        self.submit_button = PushButton("Submit", self, row=0, col=1)
            
        if self.show_buttons:
            self.layout.add_widget(self.clear_button)
            self.layout.add_widget(self.submit_button)
        self.setLayout(self.layout)
        # self.show()
    
    def add_element(self, element):
        self.layout.add_widget(element)
        if self.show_buttons:
            self.update_clear_submit_button_location()
    
    def add_elements(self, *elements):
        for element in elements:
            self.add_element(element)

    def update_clear_submit_button_location(self):
        self.clear_button.row = self.layout.rowCount()
        self.submit_button.row = self.layout.rowCount()
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.clear_button)
    
    def show_primary_buttons(self):
        self.show_buttons = True
        self.update_clear_submit_button_location()

    def add_layout(self, layout):
        self.layout.add_layout(layout)