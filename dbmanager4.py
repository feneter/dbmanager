# improvement from dbmanager3
#more shot functions
#debug dbmanager3

import sys
import os
import re
import time
from PyQt5.QtCore import QTimer
# organize imports. you can use a tuple, at least
from PyQt5.QtWidgets import (
    QMainWindow, QFormLayout,QAction,QDialog,QFileDialog,QFormLayout,
    QTextEdit,QListWidget,QLabel,QMenu,QWidget,QHBoxLayout,QLineEdit,
    QApplication,QVBoxLayout,QPushButton,qApp,QMenu,QGroupBox,
    QGridLayout)

from dbsource2 import DBSource
from student import Student
from widgets.push_button import PushButton
from widgets.grid_layout import GridLayout
from widgets.line_edit import LineEdit
from widgets.form import Form
from widgets.horizontal_layout import HorizontalLayout
from widgets.list_widget import ListViewWidget
from widgets.label import Label

class DBManager(QWidget ):
    def __init__(self):
        self.dbsource = DBSource()
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.main_layout=QVBoxLayout(self)
        self.main_layout.addWidget(self.search_form)
        self.Main_window()
        self.setGeometry(500,500,500,300)
        self.setWindowTitle("Students Data")
        self.updateWindowTitle()
        self.tempo_dict={}
        self.show()
                

    #main window
    def Main_window(self):
        # landing page form
        self.landing_page_form = Form(self)
        self.results=ListViewWidget(self, row=1, col=0, row_span=1, col_span=2) # listview area

        view_btn=PushButton("View Table", self,  click_slot= self.load_student_edit_form, col=0, row=2,)
        self.open_btn = PushButton("Open",self, row=2, col=1)
        self.open_btn.setMenu(self.databases_popup)
        crt_btn=PushButton("Create Table", self, col=0, row=3, click_slot=self.createtable_window)
        
        self.landing_page_form.add_elements(view_btn, self.open_btn, crt_btn, self.results)
        
        self.main_layout.addWidget(self.landing_page_form)
    
    @property
    def search_form(self):
        search_form = Form(self, show_primary_buttons=False)
        # search form
        self.SSname=LineEdit(self, 0, 0)
        srch_btn=PushButton("Search", self, 0, 1, click_slot=self.retrive_data)
        search_form.add_elements(srch_btn, self.SSname)
        return search_form

    #createtable window
    def createtable_window(self):
        self.hide_widget(self.landing_page_form)
        self.col_input_form = Form(self)
        self.main_layout.addWidget(self.col_input_form)
        self.col_no=LineEdit(self, row=1, col=0)
        self.submit_btn=PushButton('Submit', self, row=1, col=1, click_slot=self.get_columns)
        self.col_input_form.add_elements(self.col_no, self.submit_btn)

    #modification window
    def modify_window(self):
        self.get_user_columns()
        self.hide_widget(self.landing_page_form)
        
        form_layout = QFormLayout(self)
        for key,value in self.tempo_dict.items():
            form_layout.addRow(QLabel(value,self),QLineEdit(self))
        self.tempo_dict.clear()
    
    @property
    def student_form_buttons(self):
        buttons_layout = HorizontalLayout(row=5, row_span=1, col_span=2)

        self.Submitbtn = PushButton("Submit", self, click_slot=self.get_new_data)
        Deletebtn = PushButton("Delete", self, click_slot=self.delete_all_data)
        Cancelbtn = PushButton("Cancel", self, click_slot=self.cancel_operation)
        buttons_layout.add_elements(self.Submitbtn, Cancelbtn, Deletebtn)
        return buttons_layout

    def load_student_edit_form(self):
        self.hide_widget(self.landing_page_form)
        self.student_form = Form(self)
        self.Notice = Label("NOTE:", self, row=0, col=0, col_span=2, row_span=1)
        self.student_form.add_element(self.Notice)
        self.SName = LineEdit(self, row=1, col=1)
        self.SId = LineEdit(self, row=2, col=1)
        self.SAge = LineEdit(self, row=3, col=1)
        self.SMajor = LineEdit(self, row=4, col=1)

        self.student_form.add_elements(self.SName, self.SId, self.SAge, self.SMajor)
        labels = ["Name", "ID", "Age", "Major"]
        for row, label in enumerate(labels, start=1):
            self.student_form.add_element(Label(label, self, row=row, col=0))
        self.student_form.add_layout(self.student_form_buttons)
        self.main_layout.addWidget(self.student_form)

    #this colects columns name sa specified by user so to create table
    def get_columns(self):
        from PyQt5.QtCore import QRect
        try:
            columns = self.main_layout.itemAt(2)
            self.main_layout.removeItem(columns)
            columns.setGeometry(QRect(0, 0, 0, 0))
        except:
            pass
        finally:
            self.column_names_form = Form(self)
            cols=int(self.col_no.text())
            self.tempo_dict={}
            column_names = QFormLayout(self)
            for i in range(1, cols+1):
                col_key=QLineEdit(self)
                self.tempo_dict[col_key]=''
                column_names.addRow(QLabel(f"Column {i}",self),col_key)
            self.column_names_form.layout.addLayout(column_names, 0, 0)

            create_btn=PushButton("Create",self, row=1, col=0, row_span=1, col_span=2, click_slot=self.modify_window)
            self.column_names_form.add_element(create_btn)
            self.main_layout.addWidget(self.column_names_form)
            
    #this picks datbase file thart exist in databse folder
    @property
    def databases_popup(self):
        menu=QMenu(self)
        if not self.dbsource.available_databases:
            menu.addAction("No databases")
            return menu

        for f in  self.dbsource.available_databases:
            action=menu.addAction(f)
            action.triggered.connect(self.pull_dbfile)
        return menu

    #this pulls bdfile and asign if ready to be used in database system       
    def pull_dbfile(self):
        source=self.sender() # origin of signal
        self.dbsource.change_db(source.text())
        self.updateWindowTitle()
        self.Present_Table()

    #this pick new data from edit window 
    def get_new_data(self):
        print(self.SName.text())
        Sdata=Student(self.SName.text(),self.SId.text(),self.SAge.text(),self.SMajor.text())
        self.dbsource.insert_data_as_tuple(Sdata)
        self.clear_fields(self.SName,self.SId,self.SAge,self.SMajor)

    #this read data from the database and present them on the view
    def retrive_data(self):
        self.dbsource.select_all(self.SSname.text())
        try:
            self.hide_widget(self.landing_page_form)
        except:
            pass
        if not self.dbsource.container:
            self.Notice.clear()
            self.Notice.setText(f"No results found for : {self.SSname.text()}")
            self.Notice.setStyleSheet("color:red")                
            return
        self.SName.setText(self.dbsource.container[0])
        self.SId.setText(self.dbsource.container[1])
        self.SAge.setText(str(self.dbsource.container[2]))
        self.SMajor.setText(self.dbsource.container[3])
        try:
            self.Submitbtn.clicked.disconnect(self.get_new_data)
            self.Submitbtn.setText("Update")
            self.Submitbtn.clicked.connect(self.Update_chages)
        except :
            pass
        self.dbsource.container.clear()

    #this update changes by picking updates from display section
    def Update_chages(self):
        self.Submitbtn.setText("Submit")
        self.Submitbtn.clicked.disconnect(self.Update_chages)
        self.Submitbtn.clicked.connect(self.get_new_data)
        Modified_data = Student(self.SName.text(),self.SId.text(),self.SAge.text(),self.SMajor.text())
        print(Modified_data)
        self.dbsource.update_data(Modified_data,self.SSname.text())
        self.clear_fields(self.SSname,self.SName,self.SId,self.SAge,self.SMajor)

    #this cleans the edit field as well delete target content from database
    def delete_all_data(self):
        self.dbsource.delete_by_name(self.SSname.text())
        self.clear_fields(self.SSname,self.SName,self.SId,self.SAge,self.SMajor)

    #this read all table from database and present it on display
    def Present_Table(self):
        self.clear_fields(self.results, self.dbsource.ss)
        self.dbsource.read_all()
        for row in self.dbsource.ss:
            self.results.addItem(str(row))

    #this cancels operation    and return to the main window
    def cancel_operation(self):
        try:
            self.hide_widget(self.student_form)
        except AttributeError as e:
            print("this replace any previous widget to home widget")
        finally:
            self.Main_window()

    #this removes formar widget ready to add new one
    def hide_widget(self,widget):
        self.main_layout.removeWidget(widget)
        widget.hide()

    #this stores the column name specified by user so to be used later
    def get_user_columns(self):
        for key,val in self.tempo_dict.items():
            self.tempo_dict[key]=key.text()
            
    #this clear contenst ni various field or methods
    def clear_fields(self,*fields):
        for field in fields:
            field.clear()
                

    def updateWindowTitle(self):
        win_title =self.windowTitle()
        new_title = f"{win_title.split(' - ')[0]} - {self.dbsource.using_database}"
        self.setWindowTitle(new_title)

if __name__=='__main__':
    app=QApplication(sys.argv)
    db=DBManager()
    sys.exit(app.exec_())



