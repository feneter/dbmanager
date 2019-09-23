from PyQt5.QtWidgets import QWidget ,QFormLayout,QLineEdit,QLabel,QVBoxLayout
from widgets.push_btn import  Pushbutton
from widgets.label import Label
from widgets.grid_layout import Gridlayout
from widgets.form_layout import Formlayout
from widgets.line_edit import Linedit
from widgets.form import Form
from PyQt5.QtCore import QRect

class userForm(QWidget):
    def __init__(self):
        super().__init__()
        self.column_dict={}
        self.field_dict={}
        self.col_num=0

    def get_columns_number(self,layout1,slot):
        self.form=Form(self)
        self.tabel_name=Linedit(self,row=0,col=1)
        self.col_num=Linedit(self,row=1,col=1)
        btn=Pushbutton("submit",self,row=2,col=1,click_slot=slot)
        self.form.add_elements(Label(self,"Table name:",row=0,col=0),self.tabel_name,Label(self,"Enter columns number:",row=1,col=0),self.col_num,btn)
        layout1.addWidget(self.form)

    # def dropdown_cols(self):
    #     try:
    #         cols=layout1.itemAt(2)
    #         layout1.removeItem(cols)
    #         cols.setGeometry(QRect(0,0,0,0))
    #     except:
    #         pass
    #     finally:
    #         form=QVBoxLayout(self)
    #         grid=Gridlayout(self)
    #     for i in range(int(self.col_num.text())):
    #         name=Linedit(self,row=i,col=1)
    #         self.column_dict[name]=""
    #         grid.add_widgets(Label(self,f"column {i}",row=i,col=2),name)
    #         i+=0
    #     form.addLayout(grid)
    #     self.form.layout.addWidget(form)

    def dropdown_cols(self):
        # try:
        #     cols=layout1.itemAt(2)
        #     layout1.removeItem(cols)
        #     cols.setGeometry(QRect(0,0,0,0))
        # except:
        #     pass
        # finally:
        form=Formlayout(self)
        for i in range(int(self.col_num.text())):
            name=Linedit(self)
            self.column_dict[name]=""
            grid.add_widgets(Label(self,f"column {i}"),name)
            i+=0
        self.form.layout.addWidget(form)
    
    

    def get_columns_names(self):
        for key, value in self.column_dict.items():
            self.column_dict[key]=key.text()
    
    def create_user_form(self):
        form=Formlayout(self)
        for key in self.column_dict:
            field=Linedit(self)
            form.addRow(Label(self.column_dict.get(key)),field)
            self.field_dict[field]=''

    def get_columns_fields(self):
        for key in self.field_dict:
            self.field_dict[key]=key.text()
    