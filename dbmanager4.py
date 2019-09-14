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

class DBManager(QWidget ):
    def __init__(self):
        self.dbsource = DBSource()
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.main_layout=QVBoxLayout(self)
        self.Main_window()
        self.setGeometry(500,500,500,300)
        self.setWindowTitle("Students Data")
        self.updateWindowTitle()
        self.tempo_dict={}
        self.show()
                

    #main window
    def Main_window(self):
        self.search_form = Form(self, show_primary_buttons=False)
        self.main_layout.addWidget(self.search_form)

        self.sub_widget1=QWidget(self)
        grid=GridLayout(self)
        self.add_widget(self.sub_widget1,grid)
        
        srch_bar=LineEdit(self, 0, 0)
        self.search_form.add_element(srch_bar)
        self.pick_db_file()
        srch_btn=PushButton("Search", self, 0, 1)
        self.search_form.add_element(srch_btn)


        self.results=QListWidget(self)
        grid.addWidget(self.results, 1,0,1,2)

        view_btn=PushButton("View Table", self,  click_slot= self.modify_window, col=0, row=2,)
        grid.add_widget(view_btn)
        
        self.open_btn = PushButton("Open",self, click_slot=self.pick_db_file, row=2, col=1)
        self.open_btn.setMenu(self.menu)
        grid.add_widget(self.open_btn)

        crt_btn=self.create_button("Create Table", self.createtable_window)
        grid.addWidget(crt_btn, 3,0)


    #createtable window
    def createtable_window(self):

        self.replace_widget(self.sub_widget1)
        self.sub_widget2=QWidget(self)
        self.grid=QGridLayout(self)
        self.add_widget(self.sub_widget2,self.grid)

        self.main_layout.addWidget(self.sub_widget2)

        TName=QLineEdit(self)
        self.grid.addWidget(TName,0,0,1,2)

        self.col_no=QLineEdit(self)
        self.grid.addWidget(self.col_no,1,0)

        self.submit_btn=QPushButton('submit',self)
        self.submit_btn.clicked.connect(self.get_columns)
        self.grid.addWidget(self.submit_btn,1,1)

        self.sub_widget2.setLayout(self.grid)
        self.sub_widget2.show()

    #modification window
    def modify_window(self):
        self.get_user_columns()
    #make decision betwwen the edit mode or create mode onto the modification window
        try:
            if self.sub_widget1:
                print("bug here")
                self.replace_widget(self.sub_widget1)
                self.edit=True
            if self.sub_widget2:
                print("bug there")
                self.replace_widget(self.sub_widget2)
                self.edit=False
                self.create=True
        except AttributeError as e:
            print("cant replace widget tha is not created")

        self.sub_widget3=QWidget(self)
        Glayout=QGridLayout(self)
        self.add_widget(self.sub_widget3,Glayout)

        #search section in modification window
        LMname=QLabel("Enter name:",self)
        Glayout.addWidget(LMname, 0,0)
        self.SSname=QLineEdit(self)
        Glayout.addWidget(self.SSname, 0,1)
        Searchbtn=QPushButton("Search",self)
        Searchbtn.clicked.connect(self.retrive_data)
        Glayout.addWidget(Searchbtn, 0,2)
        
        #edit mode in modification window
        if self.edit:
            self.Notice=QLabel("NOTE:",self)
            Glayout.addWidget(self.Notice, 1,1)
            self.SName = QLineEdit(self)
            self.SId = QLineEdit(self)
            self.SAge = QLineEdit(self)
            self.SMajor = QLineEdit(self)
            self.College = QLineEdit(self)
            form_elements = [("Name", self.SName), ("College", self.College), ("ID", self.SId), ("Age", self.SAge), ("Major", self.SMajor)]
            row = 2
            for element in form_elements: 
                label, field = element    
                self.add_widget_to_grid_layout(QLabel(label, self), Glayout, row, 0)
                self.add_widget_to_grid_layout(field, Glayout, row, 1)
                row += 1
            
            num=5
        #create mode in modification window
        elif self.create:
            form_layout=QFormLayout(self)
            for key,value in self.tempo_dict.items():
                form_layout.addRow(QLabel(value,self),QLineEdit(self))
            Glayout.addLayout(form_layout,1,0,1,3)
            num=int(self.col_no.text())+1

        #modification window buttons
        self.Submitbtn = self.create_button("Submit", self.get_new_data)
        Deletebtn = self.create_button("Delete", self.delete_all_data)
        Cancelbtn = self.create_button("Cancel", self.cancel_operation)
        self.tempo_dict.clear()
        self.add_widget_to_grid_layout(self.Submitbtn, Glayout, num, 0)
        self.add_widget_to_grid_layout(Cancelbtn, Glayout, num, 2)
        self.add_widget_to_grid_layout(Deletebtn, Glayout, num, 1)
        
    def add_widget_to_grid_layout(self, widget, grid, row, col, row_span=0, col_span=0):
        """helper method to add widgets to grid layout"""
        grid.addWidget(widget, row, col)

    def create_button(self, label, slot):
        btn = QPushButton(label, self)
        btn.clicked.connect(slot)
        return btn

    #this picks datbase file thart exist in databse folder
    def pick_db_file(self):
        self.menu=QMenu(self)
        for file in  os.scandir(r'./'):
            partten=r'(\.db)$'
            matches=re.findall(partten,file.name)
            for _ in  range(len(matches)):
                action=self.menu.addAction(file.name)
                action.triggered.connect( self.pull_dbfile)

    #this pulls bdfile and asign if ready to be used in database system       
    def pull_dbfile(self):
        source=self.sender() # origin of signal
        self.dbsource.change_db(source.text())
        self.search_form.show_primary_buttons()
        self.updateWindowTitle()
        self.Present_Table()

    #this pick new data from edit window 
    def get_new_data(self):
        print(self.SName.text())
        Sdata=Student(self.SName.text(),self.SId.text(),self.SAge.text(),self.SMajor.text())
        self.dbsource.insert_data_as_tuple(Sdata)
        self.clear_field(self.SName,self.SId,self.SAge,self.SMajor)

    #this read data from the database and present them on the view
    def retrive_data(self):
        self.dbsource.select_all(self.SSname.text())
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
        self.clear_field(self.SSname,self.SName,self.SId,self.SAge,self.SMajor)

    #this cleans the edit field as well delete target content from database
    def delete_all_data(self):
        self.dbsource.delete_by_name(self.SSname.text())
        self.clear_field(self.SSname,self.SName,self.SId,self.SAge,self.SMajor)

    #this read all table from database and present it on display
    def Present_Table(self):
        self.clear_field(self.results, self.dbsource.ss)
        self.dbsource.read_all()
        for row in self.dbsource.ss:
            self.results.addItem(str(row))
        print("Table presented")

    #this cancels operation    and return to the main window
    def cancel_operation(self):
        try:
            self.replace_widget(self.sub_widget1)
            self.replace_widget(self.sub_widget2)
            self.replace_widget(self.sub_widget3)

        except AttributeError as e:
            print("this replace any previous widget to home widget")
        finally:
            self.Main_window()

    #this colects columns name sa specified by user so to create table
    def get_columns(self):
        from PyQt5.QtCore import QRect
        cols=int(self.col_no.text())
        layout_item=self.grid.itemAtPosition(2,0)
        if layout_item:
            print(layout_item.itemAt(0).widget().text())               
            self.grid.removeItem(layout_item)
            layout_item.setGeometry(QRect(0,0,0,0))
        self.tempo_dict={}
        form_layout=QFormLayout(self)
        for i in range(cols):
            col_key=QLineEdit(self)
            self.tempo_dict[col_key]=''
            form_layout.addRow(QLabel(f"Column {i+1}",self),col_key)
        self.grid.addLayout(form_layout,2,0,1,2)

        create_btn=QPushButton("create",self)
        create_btn.clicked.connect(self.modify_window)
        self.grid.addWidget(create_btn,3,0,1,2)

    #this removes formar widget ready to add new one
    def replace_widget(self,widget):
        self.main_layout.removeWidget(widget)
        widget.hide()

    #this add new widget to main layout
    def add_widget(self,widget,layout):
        self.main_layout.addWidget(widget)
        widget.setLayout(layout)
        widget.show()

    #this stores the column name specified by user so to be used later
    def get_user_columns(self):
        for key,val in self.tempo_dict.items():
            self.tempo_dict[key]=key.text()
            
    #this clear contenst ni various field or methods
    def clear_field(self,*fields):
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



