#
class Student:
    """this is general class for students contents
    """
    def __init__(self,Name,Id=None,Age=None,Major=None):
        self.Name =Name
        self.Id = Id
        self.Age=Age
        self.Major=Major

    #providing format of content from class
    def __str__(self):
        return f"{{Name:{self.Name},Id:{self.Id},Age:{self.Age},Major:{self.Major}}}"
