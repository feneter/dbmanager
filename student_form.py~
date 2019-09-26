from dbsource2 import DBsource
from widgets.form import Form
from widgets.label import Label
from widgets.push_btn import Pushbutton
from widgets.line_edit import Linedit
from widgets.horizontal_layout import HorizontalLayout
from PyQt5.QtWidgets import QWidget


class studentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.name=Linedit(self,row=0,col=1)
        self.id=Linedit(self,row=1,col=1)
        self.age=Linedit(self,row=2,col=1)
        self.major=Linedit(self,row=3,col=1)

    def set_student_form(self,layout):
        form=Form(self)
        labels=["Name","Id","Age","Major"]
        fields=[self.name,self.id,self.age,self.major]
        row=0
        for label in labels:
            form.add_elements(Label(self,label,row=row,col=0),fields[row])
            row+=1
        return layout.addWidget(form)
        
    
    def set_form_buttons(self,layout,submit_slot,delete_slot,cancel_slot):
        box=HorizontalLayout(self)
        submit_btn=Pushbutton("submit",self,click_slot=submit_slot)
        delete_btn=Pushbutton("Delete",self,click_slot=delete_slot)
        cancel_btn=Pushbutton("Cancel",self,click_slot=cancel_slot)
        box.add_elements(submit_btn,delete_btn,cancel_btn)
        return layout.addLayout(box)
