from botfile import BotFile

class Log():
    """Class for keeping logs. 

    Attributes:
        file -- the file object to write the logs
    """
    __file = BotFile()

    def __init__(self):
        self.__file.setFileName("bot.log")

    def log(self, message):
        """Appends the message to the log file.
        Accepts string, int, double.
        """
        self.__file.appendFile(["", message])