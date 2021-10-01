import re
import requests
import json
import datetime

from turkish import TurkishText


class Responses:
    """Class for handling responses to messages. 

    Attributes:
        __methods -- the list of methods, contains function pointers
        __canned -- the dictionary of canned responses
    """

    __methods = []
    __canned = dict()
    __commands = dict()

    def __init__(self):
        """Adds the canned responses and command responses to the 
        respective dictionaries.
        """

        # Canned responses
        self.__canned['hello'] = "Hello from the other side"
        self.__canned['günaydın'] = "Günaydın hocam!"

        # Command responses
        self.__commands[
            '/start'] = "Merhaba! Ben ODTÜ Bot. \n\nGüncel yemekhane menüsünü öğrenmek için `/yemekhane` " \
                        "yazabilirsin. `/yemekhane yarın` komutu ile yarının menüsünü de öğrenebilirsin. Belirli bir " \
                        "tarihin yemekhane menüsünü görmek için `/yemekhane (GG-AA-YYYY)` formatını " \
                        "kullanabilirsin.\n\n`/menu` komutu ile yemekhane servisine abone olabilirsin. Bu servis ile " \
                        "haftaiçi her gün, sabah 9'da güncel yemek menüsünü özel mesaj olarak gönderiyorum." \
                        "\n\nGözüne çarpan hataları ya da botta olmasını istediğin özellikleri @frozsgy'e " \
                        "iletebilirsin.\n\nUmarım beni seversin :) "
        self.__commands[
            '/help'] = "Help will arrive for the ones who really need."

    def respond(self, message):
        """Processes the message and adds the response (if exists) to the response list.
        Returns list of responses.
        """

        message = TurkishText(message).lower()
        if message.count('@') > 0:
            message_tuple = message.split('@')
            if 'odtubot' in message_tuple:
                message = message_tuple[0]
            else:
                return []

        # Canned responses
        res = self.canned(message)

        # Command responses
        res += self.commands(message)

        # Cafeteria function
        if re.search('/yemekhane', message):
            if re.search('yarın', message):
                res.append(self.food('tomorrow'))
            elif len(message.split()) > 1:
                res.append(self.food(message.split()[1]))
            else:
                res.append(self.food())

        # Daily cafeteria menu function
        if re.search('/menu', message):
            res.append(('service', 1))

        return res

    def canned(self, message):
        """Checks the message for possible canned responses.
        Returns list of responses.
        """
        res = []
        message = TurkishText(message.strip()).lower()
        for key, val in self.__canned.items():
            if re.search(key, message):
                res.append(val)
        return res

    def commands(self, message):
        """Checks the message for possible responses to commands.
        Requires an exact match of the phrase.
        Returns list of responses.
        """
        res = []
        message = TurkishText(message.strip()).lower()
        for key, val in self.__commands.items():
            if re.search(r'^' + key + '$', message):
                res.append(val)
        return res

    def food(self, date='today'):
        """Fetches the menu offered at METU Cafeteria for today, tomorrow, or any given date.
        Returns string.
        """
        now = datetime.datetime.now()

        date_search = re.search(
            r"(0{0,1}[1-9]|[12][0-9]|3[01])[- /.](0{0,1}[1-9]|1[012])[- /.](19|20)\d\d",
            date)
        if date_search:
            date_match = re.search(r"(\d{1,2})(.*?)(\d{1,2})(.*?)(\d{4})",
                                   date)
            dates = date_match.groups()
            iday = '-'.join(dates[::2])
        else:
            if date == 'tomorrow':
                now += datetime.timedelta(days=1)
            else:
                date = 'today'
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
            if date == 'today':
                menu_response = ["🍴 Bugün yemekhanede şunlar varmış hocam:"]
            elif date == 'tomorrow':
                menu_response = ["🍴 Yarın yemekhanede şunlar varmış hocam:"]
            else:
                menu_response = [
                    "🍴 %s tarihinde yemekhanede şunlar varmış hocam:" % date
                ]
            menu_response.append("")
            menu_response.append("*Öğle Yemeği*")
            for j in range(4):
                if daily[0][j] != '*':
                    menu_response.append("· " + daily[0][j])
            menu_response.append("")
            if daily[1][0] != "*":
                menu_response.append("*Akşam Yemeği*")
                for j in range(4):
                    menu_response.append("· " + daily[1][j])
                menu_response.append("")
            if daily[0][4] != '':
                menu_response.append("🥬 Vejetaryen alternatifler:")
                menu_response.append("")
                menu_response.append("*Öğle Yemeği*")
                menu_response.append("· " + daily[0][4])
                menu_response.append("")
            if daily[1][0] != "*":
                menu_response.append("*Akşam Yemeği*")
                menu_response.append("· " + daily[1][4])
                menu_response.append("")
            menu_response.append("Afiyet olsun!")
            return '\n'.join(menu_response)
        else:
            if date == 'today':
                return "Bugün yemek yok hocam 😔"
            elif date == 'tomorrow':
                return "Yarın yemek yok hocam 😔"
            else:
                return "%s tarihinde yemek yok hocam 😔" % date
