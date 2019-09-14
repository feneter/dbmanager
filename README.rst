DBManager
=========

OOP
+++

* break student into own file
* change dbsource2 into class and all its methods and all
  its properties (four specifically: conn, c [for cursor], container and ss)
  These will now be referenced with self.connection, self.cursor, self.container and self.ss
  together with all other methods
* When we initialize the GUI app we also instantiate the DBSource, which selects the database
  and loads the initial data

OOP2
++++
* Introduces getters and setters
  When we want to access properties from classes we use a period (.) on the class
  object. This is OK in Python. We don't want to be changing properties so easily though.
  So, properties that are private, in Python are marked ``conventionally`` by
  double underscore like ``__name``.

.. topic:: Getters
    
    Methods we use to access property values from class
    In python they are decorated with @property.
    Having ``@property`` on a method will make it a property which will also be assignable

.. code:: python

    class Student:
        def __init__(self):
            self._name = "Student1

        @property
        def name(self):
            return self._name

    student = Student()
    print(student.name)
    
    # Without the @property decorator we would have used

.. code:: python

    print(student.name())


.. topic:: Setters
    
    Methods we use to assign new values

.. code:: python
    
    class Student:
        def __init__(self):
            self._name = "Student1

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, new_name):
            self._name = new_name.capitalize if new_name.startswith('j') else new_name.upper() # name is now changed

        # To change the name on the student object we will do


.. code:: python

    student = Student()
    student.name = "Baharia"

    # Without the @name.setter decorator we would have used

    student.name("Baharia")

    The setter case here is only used for demonstration. You will want a setter When
    you have a condition or other checks when assigning the new value.