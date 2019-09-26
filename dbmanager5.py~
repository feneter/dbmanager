# improvement from dbmanager3
#more shot functions
#debug dbmanager3


import sys
import os
import re
import time
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow,QFormLayout,QAction,QDialog,
    QFileDialog,QFormLayout,QTextEdit,QListWidget,QLabel,QMenu,QWidget,
    QHBoxLayout,QLineEdit,QApplication,QVBoxLayout,QPushButton,qApp,QMenu,
    QGroupBox,QGridLayout)

from dbsource2 import DBsource
from student import student
from widgets.grid_layout import Gridlayout
from widgets.form import Form
from widgets.form_layout import Formlayout
from widgets.push_btn import Pushbutton
from widgets.line_edit import Linedit
from widgets.label import Label
from widgets.horizontal_layout import HorizontalLayout
from widgets.list_widget import Listwidget
from student_form import studentForm
from custom_form import userForm


class db_source(QWidget ):
        def __init__(self):

            super().__init__()
            self.dbsource=DBsource()
            self.main_layout=QVBoxLayout(self)
            self.user=userForm(self.main_layout)
            self.student=studentForm(self.main_layout)
            self.initUI()

        def initUI(self):
            self.searchForm=self.search_form()
            self.main_layout.addWidget(self.searchForm)
            self.Main_window()
            self.setGeometry(500,500,500,300)
            self.setWindowTitle('Students_Data')
            self.tempo_dict={}
            self.user_dict={}
            self.show()           


#main window
        def Main_window(self):
            self.landing_page_form= Form(self)
            self.results=Listwidget(self,row=1,col=0,row_span=1,col_span=2)
            view_btn=Pushbutton("view table",self,2,0,click_slot=self.default_form)
            self.open_btn=Pushbutton("open",self,2,1)
            self.open_btn.setMenu(self.databases_popup())
            create_btn=Pushbutton("create table",self,3,0,click_slot=self.createtable_window)
            self.landing_page_form.add_elements(self.results,view_btn,self.open_btn,create_btn)
            self.main_layout.addWidget(self.landing_page_form)


            
#createtable window
        def createtable_window(self):
            self.hide_widget(self.searchForm)
            self.hide_widget(self.landing_page_form)
            self.user.get_columns_number()
        
        def default_form(self):
            self.hide_widget(self.landing_page_form)
            self.student.set_student_form()
            self.student.set_form_buttons(self.get_new_data,self.delete_all_data,self.return_home)

        def return_home(self):
            self.hide_widget(self.student.set_student_form())
            self.hide_layout(self.student.set_form_buttons())
            self.Main_window()

            
        def pick_db_file(self):
            """sort any file with .db extension from database folder and creates menu widget
            """
            self.menu=QMenu(self)
            for file in  os.scandir(r'/home/judethaddeus/myprojects/py_projects/dbmanager'):
                partten=r'(\.db)$'
                matches=re.findall(partten,file.name)
                for _ in  range(len(matches)):
                    action=self.menu.addAction(file.name)
                    action.triggered.connect( self.pull_dbfile)

        def pull_dbfile(self):
            """assigns the selected dbfile to the databes query
            """
            source=self.sender()
            self.dbsource.change_db(source.text())
            self.updateWidowTitle()
            self.Present_Table()

        def get_new_data(self):
            """picks new data from user and save them to database directly
            """
            print(self.name.text())
            Sdata=student(self.name.text(),self.id.text(),self.age.text(),self.major.text())
            self.dbsource.insert_data_tuple(Sdata)
            self.clear_field(self.name,self.id,self.age,self.major)
        
#this read data from the database and present them on the view
        def retrive_data(self):
            """reads records from database and display them on window
            """
            self.dbsource.container1
            self.dbsource.Select_allData(self.srch_name.text())
            if not self.dbsource.container1:
                self.Notice.clear()
                self.Notice.setText(f"No results found for : {self.srch_name.text()}")
                self.Notice.setStyleSheet("color:red")                
                return
            self.name.setText(self.dbsource.container1[0])
            self.id.setText(self.dbsource.container1[1])
            self.age.setText(str(self.dbsource.container1[2]))
            self.major.setText(self.dbsource.container1[3])
            try:
                self.Submitbtn.clicked.disconnect(self.get_new_data)
                self.Submitbtn.setText("Update")
                self.Submitbtn.clicked.connect(self.Update_chages)
            except :
                pass
            self.dbsource.container1.clear()

        def Update_chages(self):
            """update the database from user modification and save them
            """
            self.Submitbtn.setText("Submit")
            self.Submitbtn.clicked.disconnect(self.Update_chages)
            self.Submitbtn.clicked.connect(self.get_new_data)
            Modified_data=student(self.name.text(),self.id.text(),self.age.text(),self.major.text())
            print(Modified_data)
            self.dbsource.update_data(Modified_data,self.srch_name.text())
            self.clear_field(self.srch_name,self.name,self.id,self.age,self.major)

        def delete_all_data(self):
            """delete records from database file and clear fields on disply
            """
            self.dbsource.delete_data_Name(self.srch_name.text())
            self.clear_field(self.srch_name,self.name,self.id,self.age,self.major)

        def Present_Table(self):
            """gets all records from the table and disply on window
            """
            self.clear_field(self.results,self.dbsource.container2)
            self.dbsource.read_all()
            for row in self.dbsource.container2:
                self.results.addItem(str(row))
            print("Table presented")


#this stores the column name specified by user so to be used later
        def get_user_columns(self):
            for key,val in self.tempo_dict.items():
                self.tempo_dict[key]=key.text()

#this clear contenst ni various field or methods
        def clear_field(self,*fields):
            for field in fields:
                field.clear()

#change the window title   
        def updateWidowTitle(self):
            win_title=self.windowTitle()
            new_title=f"{win_title.split('-')[0]}-{self.dbsource.using_db}"
            self.setWindowTitle(new_title)
             
        def search_form(self):
            search_form=Form(self,show_primary_buttons=False)
            self.srch_name=Linedit(self,0,0)
            srch_btn=Pushbutton("serch",self,0,1,click_slot=self.retrive_data)
            search_form.add_elements(srch_btn,self.srch_name)
            return search_form
        
        def databases_popup(self):
            menu=QMenu(self)
            if not self.dbsource.available_database():
                menu.addAction("No database")
                return menu
            for f in self.dbsource.available_database():
                action=menu.addAction(f)
                action.triggered.connect(self.pull_dbfile)
            return menu

        def hide_widget(self,widget):
            self.main_layout.removeWidget(widget)
            widget.hide()
            widget.setGeometry(QRect(0,0,0,0))
            print("widget hidden")

        def hide_layout(self,layout):
            self.main_layout.removeItem(layout)
            layout.setGeometry(QRect(0,0,0,0))


if __name__=='__main__':
        app=QApplication(sys.argv)
        db=db_source()
        sys.exit(app.exec_())



