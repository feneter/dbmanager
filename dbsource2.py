import sqlite3
import os
from PyQt5.QtWidgets import QFileDialog
 

class DBsource:
        """this class is for overall db-crud operations
        """
        def __init__(self,filename=""):
                """this is db_constructor that is initialized instantl object is created
                """
                self.using_db= filename if filename else "Example.db"
                self.connection=sqlite3.Connection(self.using_db)
                self.cursor=self.connection.cursor()
                self.container1=[]
                self.container2=[]
                self.create_table('Students_Data','name','id','age','major')
        
        
        def change_db(self, change_to_db):
                """this change db file to be used with db system to all functions
                """
                self.connection=sqlite3.Connection(change_to_db)
                self.cursor=self.connection.cursor()


        def create_table(self,tablename,col1,*colms):
                """this create table fro general puposer any name any number of columns
                """
                statment="CREATE TABLE IF NOT EXISTS {}({} BLOB"
                arg_list=[tablename,col1] 
                for colm in colms:
                        statment+=",{} BLOB"
                        arg_list.append(colm)
                statment +=")"
                command=statment.format(*arg_list)
                with self.connection:
                        self.cursor.execute(command)



        def insert_data_dictionary(self,studentObject):
                """INSERT data using dictionary format

                Data is passed as student object
                """
                with self.connection:
                        self.cursor.execute("INSERT INTO Students_Data VALUES (:Name,:ID,:Age,:Major)",{'Name':studentObject.Name,'ID':studentObject.Id,'Age':studentObject.Age,'Major':studentObject.Major})


        def insert_data_tuple(self,studentObject):
                """INSERT data using tuple format
                 
                Data is passed as student object
                """
                with self.connection:
                        self.cursor.execute("INSERT INTO Students_Data VALUES(?,?,?,?)",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major))

        def delete_data_Name(self,StudentName):
                """DELETE data from database

                Name is required
                """
                with self.connection:
                        self.cursor.execute("DELETE FROM Students_Data WHERE  Name=(?)",(StudentName,))

        def Update_data(self,studentObject,OldName):
                """UPDATE data in database

                pass Student object and old name
                """
                with self.connection:
                        self.cursor.execute("UPDATE Students_Data SET Name={},Id={},Age={},Major={} WHERE  Name={}",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major,OldName))
                                              

        def select_oneData(self,StudentName ,Particular):
                """Select one record that matches name
                pass Name and particular
                """
                with self.connection:
                        self.cursor.execute("SELECT {} FROM Students_Data WHERE Name={}",(Particular,StudentName))
                        return self.cursor.fetchall()



        def Select_allData(self,StudentName):
                """select all records in table that matches name from db

                pass Name
                """
                with self.connection:
                        self.cursor.execute("SELECT * FROM Students_Data WHERE Name=(?)",(StudentName,))
                        for item in  self.cursor.fetchall() :
                                for detail in item:
                                        self.container1.append(detail)


        def read_all(self):
                """select all records from table
                returns a list
                """
                if self.container2: self.container2.clear()
                with self.connection:
                        for f in self.cursor.execute("SELECT * FROM Students_Data "):
                                self.container2.append(f)
        
        def available_database(self):
                import glob
                return glob.glob('*.db')

