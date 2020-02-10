class TurkishText():
    """Class for handling lowercase/uppercase conversions of Turkish characters..

    Attributes:
        text -- Turkish text to be handled
    """

    text = ""
    l = ['ı', 'ğ', 'ü', 'ş', 'i', 'ö', 'ç']
    u = ['I', 'Ğ', 'Ü', 'Ş', 'İ', 'Ö', 'Ç']

    def __init__(self, text):
        self.text = text

    def upper(self):
        """Converts the text into uppercase letters.
        Returns string.
        """
        res = ""
        for i in self.text:
            if i in self.l:
                res += self.u[self.l.index(i)]
            else :
                res += i.upper()
        return res

    def lower(self):
        """Converts the text into lowercase letters.
        Returns string.
        """
        res = ""
        for i in self.text:
            if i in self.u:
                res += self.l[self.u.index(i)]
            else :
                res += i.lower()
        return res

    def capitalize(self):
        """Converts each first letter to uppercase, and the rest to lowercase letters.
        Returns string.
        """
        m = self.text.split()
        res = ""
        for i in m:
            res += TurkishText(i[0]).upper() + TurkishText(i[1:]).lower() + " "
        return res[:-1:]
