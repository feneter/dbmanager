import sqlite3
import os
from PyQt5.QtWidgets import QFileDialog
 
#this is general class for students contents
class Student:
    def __init__(self,Name,Id=None,Age=None,Major=None):
        self.Name =Name
        self.Id = Id
        self.Age=Age
        self.Major=Major

#providing format of content from class
    def __str__(self):
        return f"{{Name:{self.Name},Id:{self.Id},Age:{self.Age},Major:{self.Major}}}"

#get database file so to be used for db-progress
def get_dbFile(FileName=None):
        if not FileName:
                print("me in use")
                return sqlite3.connect('Example.db')

        else:
                print("huku niko " + FileName)
                return sqlite3.connect(FileName)
        
conn=get_dbFile()
c=conn.cursor()

# CREATE  TABLE /general base on user options
def create_table(tablename,col1,*colms):
        statment="CREATE TABLE IF NOT EXISTS {}({} BLOB"
        arg_list=[tablename,col1] 
        for colm in colms:
                statment+=",{} BLOB"
                arg_list.append(colm)
        statment +=")"
        command=statment.format(*arg_list)
        with conn:
                c.execute(command)
create_table('tablenami' ,'column1','column2')


#  INSERT data normally
# c.execute("INSERT INTO Students_Data VALUES ('Yudathadei','Y0973ETM',22,'CS')")

#  INSERT data using dictionary format
def Insert_data_dictionary(studentObject):
        with conn:
                c.execute("INSERT INTO Students_Data VALUES (:Name,:ID,:Age,:Major)",{'Name':studentObject.Name,'ID':studentObject.Id,'Age':studentObject.Age,'Major':studentObject.Major})

#  INSERT data using tuple format
def Insert_data_tuple(studentObject):
        with conn:
                c.execute("INSERT INTO Students_Data VALUES(?,?,?,?)",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major))
#  DELETE data
def Delete_data_Name(StudentName):
        with conn:
                c.execute("DELETE FROM Students_Data WHERE  Name={}",(StudentName,))
#  UPDATE data
def Update_data(studentObject,OldName):
        with conn:
                 c.execute("UPDATE Students_Data SET Name={},Id={},Age={},Major={} WHERE  Name={}",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major,OldName))
                                              
#  SELECT only one item
def Select_oneData(StudentName ,Particular):
        with conn:
                c.execute("SELECT {} FROM Students_Data WHERE Name={}",(Particular,StudentName))
                return c.fetchall()

container=[]
#select all data
def Select_allData(StudentName):
        with conn:
                c.execute("SELECT * FROM Students_Data WHERE Name={}",(StudentName,))
                for item in  c.fetchall() :
                        for detail in item:
                                container.append(detail)
#Read all table content
ss=[]
def Read_all_contents():
        ss.clear()
        with conn:
                for f in c.execute("SELECT * FROM Students_Data "):
                        ss.append(f)
                    

