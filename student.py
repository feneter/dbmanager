class student:
    """the default class for student 
    """
    def __init__(self,Name,Id=None,Age=None,Major=None):
        self.Name=Name
        self.Id=Id
        self.Age=Age
        self.Major=Major
    #string formating
    def __str__(self):
        return f"{{Name:{self.Name},Id:{self.Id},Age:{self.Age},Major:{self.Major}}}"
    
    @property
    def Name(self):
        return self._Name
    
    @Name.setter
    def Name(self,name):
        self.__Name=name.capitalize()

    @property
    def Major(self):
        return self.__Major

    @Major.setter
    def Major(self, new_major):
        self.__Major= new_major.capitalize() if new_major.startswith('k') else new_major

if __name__ == '__main__':
    student=student("Anne","2019-02-003123",19,"k-Commerse")
    print(student.Major)
    print(student.Name)
    student.Major="a-Computer Tech"
    print(student.Major)
    student.Major="kT Security"
    print(student.Major)
