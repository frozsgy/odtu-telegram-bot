class TurkishText:
    """Class for handling lowercase/uppercase conversions of Turkish characters..

    Attributes:
        text -- Turkish text to be handled
    """

    text = ""
    lowercase = ['ı', 'ğ', 'ü', 'ş', 'i', 'ö', 'ç']
    uppercase = ['I', 'Ğ', 'Ü', 'Ş', 'İ', 'Ö', 'Ç']

    def __init__(self, text):
        self.text = text

    def upper(self):
        """Converts the text into uppercase letters.
        Returns string.
        """
        res = ""
        for i in self.text:
            if i in self.lowercase:
                res += self.uppercase[self.lowercase.index(i)]
            else:
                res += i.upper()
        return res

    def lower(self):
        """Converts the text into lowercase letters.
        Returns string.
        """
        res = ""
        for i in self.text:
            if i in self.uppercase:
                res += self.lowercase[self.uppercase.index(i)]
            else:
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
