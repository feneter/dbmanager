from PyQt5.QtWidgets import QWidget ,QFormLayout,QLineEdit,QLabel,QVBoxLayout,QPushButton
from widgets.push_btn import  Pushbutton
from widgets.label import Label
from widgets.grid_layout import Gridlayout
from widgets.form_layout import Formlayout
from widgets.line_edit import Linedit
from widgets.form import Form
from PyQt5.QtCore import QRect
from student_form import studentForm as btn

class userForm(QWidget):
    def __init__(self,layout):
        super().__init__()
        self.layout=layout
        self.col_num=Linedit(self,row=1,col=1)
        self.column_dict={}
        self.field_dict={}

        

    def get_columns_number(self):
        self.form=Form(self)
        self.tabel_name=Linedit(self,row=0,col=1)
        btn=Pushbutton("submit",self,row=2,col=1,click_slot=self.dropdown_cols)
        self.form.add_elements(Label(self,"Table name:",row=0,col=0),self.tabel_name,Label(self,"Enter columns number:",row=1,col=0),self.col_num,btn)
        self.layout.addWidget(self.form)
        return self.form

    def dropdown_cols(self):
        prev_field=self.layout.itemAt(1)
        if prev_field:
            self.hide_layout(prev_field)
        self.Form=QFormLayout()
        for i in range(int(self.col_num.text())):
            name=QLineEdit()
            self.column_dict[name]=""
            self.Form.addRow(QLabel(f"column {i+1}"),name)
            i+=0
        btn=QPushButton("create")
        btn.clicked.connect(self.create_user_form)
        self.Form.addRow(btn)
        self.layout.addLayout(self.Form)
        return self.Form
    
    def hide_layout(self,layout1):
        self.layout.removeItem(layout1)
        layout1.setGeometry(QRect(0,0,0,0))

    def hide_widget(self,widget):
        self.layout.removeWidget(widget)
        widget.hide()


    def get_columns_names(self):
        for key, value in self.column_dict.items():
            self.column_dict[key]=key.text()
    
    def create_user_form(self):
        self.get_columns_names()
        self.hide_widget(self.form)
        self.hide_layout(self.Form)
        form=QFormLayout()
        for key in self.column_dict:
            field=Linedit(self)
            form.addRow(Label(self,self.column_dict.get(key)),field)
            self.field_dict[field]=''
        self.layout.addLayout(form)
        self.layout.addLayout(btn.set_form_buttons(self))

    def get_columns_fields(self):
        for key in self.field_dict:
            self.field_dict[key]=key.text()

 
        
    