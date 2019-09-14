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