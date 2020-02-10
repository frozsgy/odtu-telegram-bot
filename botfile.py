import pathlib 
from exceptions import FileError
from locations import Locations

class BotFile():
    """Class for reading and writing a local file.

    Attributes:
        fileName -- the file name to store data
        location -- the absolute location for the bot
    """
    __location = Locations().runningFolder
    __fileName = 'offsets.ini'

    def setFileName(self, name):
        self.__fileName = name

    def fileExists(self):
        """Checks if the file exists.
        Returns boolean.
        """
        pl = pathlib.Path(self.__location + self.__fileName)
        e = pl.exists()
        if e is True and pl.is_file() :
            return True
        else :
            return False

    def writeFile(self, data):
        """Writes over with the updated details to the file.
        Takes list or tuple, and writes each element to a new line.
        """
        try:
            file = open(self.__location + self.__fileName, 'w')
            dataStr = tuple(map(str, data))
            toWrite = '\n'.join(dataStr)
            file.write(toWrite)      
        except:
            raise FileError("Cannot create file") from None

    def readFile(self):
        """Reads from the file.
        Returns a list with elements from each line.
        """
        file = open(self.__location + self.__fileName, 'r')
        lines = file.readlines()
        return [i.replace("\n","") for i in lines]

    def appendFile(self, data):
        """Appends the given data to the file.
        Takes list or tuple, and writes each element to a new line.
        """
        try:
            file = open(self.__location + self.__fileName, 'a+')
            dataStr = tuple(map(str, data))
            toWrite = '\n'.join(dataStr)
            file.write(toWrite)      
        except:
            raise FileError("Cannot create file") from None