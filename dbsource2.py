import sqlite3
import os
from PyQt5.QtWidgets import QFileDialog


class DBSource:
    """API class for the database
    Can be used to create new tables, and perform all CRUD operation on a database

    It can be initialized with a database name of choice, if not a unique database is picked
    from among databases
    """

    def __init__(self, filename=""):
        self.using_database = filename if filename else "Example.db"
        self.connection = sqlite3.connect(self.using_database)
        self.cursor = self.connection.cursor()
        self.container = []
        self.ss = []
        self.create_table('Students_Data' ,'Name','ID', "Age", "Major")

    def change_db(self, change_to_db):
        """Anytime the database changes, we also need to change the cursor
        """
        self.using_database = change_to_db
        self.connection = sqlite3.connect(change_to_db)
        self.cursor = self.connection.cursor()
        # for the sake of this, let's also make sure we have the table in this db too
        self.create_table('Students_Data' ,'Name','ID', "Age", "Major")

    # CREATE  TABLE /general base on user options
    # You would usually run statements to create database only once, or when you upgrade
    def create_table(self, tablename, col1, *cols): # at least one column
        statement="CREATE TABLE IF NOT EXISTS {}({} BLOB"
        arg_list=[tablename, col1] 
        for col in cols:
            statement+=",{} BLOB"
            arg_list.append(col)
        statement +=")"
        command=statement.format(*arg_list)
        with self.connection:
            self.cursor.execute(command)
    # we will call create_table in the constructor

    #  INSERT data using dictionary format
    def insert_data_as_dictionary(self, studentObject):
        """INSERT query uses a dictionary
        
        Data is passed in as a student object
        """
        # we can just use self.connection
        with self.connection:
            self.cursor.execute("INSERT INTO Students_Data VALUES (:Name,:ID,:Age,:Major)",{'Name':studentObject.Name,'ID':studentObject.Id,'Age':studentObject.Age,'Major':studentObject.Major})

    #  INSERT data using tuple format
    def insert_data_as_tuple(self, studentObject):
        """INSERT query uses a tuple
        
        Data is passed in as a student object
        """
        with self.connection:
            self.cursor.execute("INSERT INTO Students_Data VALUES(?,?,?,?)",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major))
    
    #  DELETE data
    def delete_by_name(self, StudentName):
        """Deletes data by name.

        Name is required
        """
        with self.connection:
            self.cursor.execute("DELETE FROM Students_Data WHERE  Name={}",(StudentName,))
    
    #  UPDATE data
    def update_data(self, studentObject,OldName):
        """Updates data for the student table

        Expects a student object and an old name
        """
        with self.connection:
            self.cursor.execute("UPDATE Students_Data SET Name={},Id={},Age={},Major={} WHERE  Name={}",(studentObject.Name,studentObject.Id,studentObject.Age,studentObject.Major,OldName))
                                        
    #  SELECT only one item 
    def select_one(self, StudentName ,Particular):
        """Selects one record that matches name

        Returns a list with one or no element
        """
        with self.connection:
            self.cursor.execute("SELECT {} FROM Students_Data WHERE Name={}",(Particular,StudentName))
            return self.cursor.fetchall() # expected this to return just one. like fetchone

    #select all data
    def select_all(self, StudentName):
        """Selects all records in a table matches a particular student

        Expects a student object

        Returns a list of all matching records found
        """
        with self.connection:
            self.cursor.execute("SELECT * FROM Students_Data WHERE Name=?",(StudentName,))
            for item in  self.cursor.fetchall() :
                for detail in item:
                    self.container.append(detail)
    
    #Read all table content
    def read_all(self):
        """Selects all records found in the database

        Returns a list
        """
        if self.ss: self.ss.clear() # only clear when there's data in
        with self.connection:
            for f in self.cursor.execute("SELECT * FROM Students_Data "):
                self.ss.append(f)
                

