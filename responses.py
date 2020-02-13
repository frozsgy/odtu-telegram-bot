import re
import requests
import json
import datetime

from turkish import TurkishText

class Responses():
    """Class for handling responses to messages. 

    Attributes:
        __methods -- the list of methods, contains function pointers
        __canned -- the dictionary of canned responses
    """

    __methods = []
    __canned = dict()

    def __init__(self):
        """Adds the canned responses to the canned responses dictionary.
        """

        #self.__methods = [self.sayHello]
        self.__canned['hello'] = "Hello from the other side"
        self.__canned['günaydın'] = "Günaydın hocam!"
        self.__canned['/start'] = "Merhaba! Ben ODTÜ Bot. Şimdilik pek fazla özelliğim yok ancak zamanla gelişeceğim. Umarım beni seversin :) "

    def respond(self, message):
        """Processes the message and adds the response (if exists) to the response list.
        Returns list of responses.
        """

        #for i in self.__methods: i(message)

        # Canned responses
        res = self.canned(message)

        # Cafeteria function
        if re.search('/yemekhane', TurkishText(message).lower()):
            if re.search('yarın', TurkishText(message).lower()):
                res.append(self.food('tomorrow'))
            else :
                res.append(self.food())

        # Help function
        if re.search('/help', TurkishText(message).lower()):
            res.append("Help will arrive for the ones who really need.")

        # Daily cafeteria menu function
        if re.search('/menu', TurkishText(message).lower()):
            res.append("PLACEHOLDERTEXTOTBEREPLACEDBYTHEBOTCLASS")

        return res

    def canned(self, message):
        """Checks the message for possible canned responses.
        Returns list of responses.
        """
        res = []
        for key, val in self.__canned.items():
            match = re.search(key, TurkishText(message).lower())
            if match:
                res.append(val)
        return res

    def food(self, date = 'today'):
        """Fetches the menu offered at METU Cafeteria for today, or tomorrow.
        Returns string.
        """
        now = datetime.datetime.now()
        if date == 'tomorrow':
            now += datetime.timedelta(days = 1)
        iday = now.strftime("%d-%m-%Y")
        url = "https://kafeterya.metu.edu.tr/service.php?tarih=" + iday
        r = requests.get(url)
        page = r.content
        items = json.loads(page)
        daily = [[], []]
        if items is not None:
            ogle = items['ogle']
            aksam = items['aksam']
            for j in range(5):
                daily[0].append(TurkishText(ogle[j]['name']).capitalize())
                daily[1].append(TurkishText(aksam[j]['name']).capitalize())
        if daily != [[], []]:
            menuResponse = ["🍴 Bugün yemekhanede şunlar varmış hocam:"]
            if date == 'tomorrow':
                menuResponse = ["🍴 Yarın yemekhanede şunlar varmış hocam:"]
            menuResponse.append("")
            menuResponse.append("*Öğle Yemeği*")
            for j in range(4):
                menuResponse.append("· " + daily[0][j])
            menuResponse.append("")
            menuResponse.append("*Akşam Yemeği*")
            for j in range(4):
                menuResponse.append("· " + daily[1][j])
            menuResponse.append("")
            menuResponse.append("🥬 Vejetaryen alternatifler:")
            menuResponse.append("")
            menuResponse.append("*Öğle Yemeği*")
            menuResponse.append("· " + daily[0][4])
            menuResponse.append("")
            menuResponse.append("*Akşam Yemeği*")
            menuResponse.append("· " + daily[1][4])
            menuResponse.append("")
            menuResponse.append("Afiyet olsun!")
            return '\n'.join(menuResponse)
        else :
            if date == 'tomorrow':
                return "Yarın yemek yok hocam 😔"
            return "Bugün yemek yok hocam 😔"

   