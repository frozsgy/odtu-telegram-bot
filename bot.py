from responses import Responses
from db import DB

import requests
import json
import datetime

class Bot():
    """Class for handling all communication with the Telegram API. 

    Attributes:
        __url -- the url for Telegram Bot API
    """

    # https://api.telegram.org/bot<token>/METHOD_NAME
    __url = "https://api.telegram.org/bot"

    def __init__(self, verbose = False, logging = False):
        self.__db = DB(verbose)
        self.__token = self.__db.get_token()
        self.__url += self.__token
        self.__r = Responses()
        self.__verbose = verbose
        self.__logging = logging

    def hello(self):
        """Tester method to check if the bot class works properly.
        """
        print("Hello, I am running nicely.")

    def get_updates(self):
        """Gets updates from the Telegram Server. Uses Long Polling.
        Returns boolean.
        """
        url = self.__url + "/getUpdates"
        offset = self.__db.get_offset()
        params = {'offset': int(offset) + 1, 
                  'limit': 100, 
                  'timeout': 0, 
                  'allowed_updates': ['message']}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok'] is True:
            res = items['result']
            for i in res:
                if 'message' in i:
                    self.parse_message(i)                    
                elif 'inline_query' in i:
                    self.parse_inline(i)
                else :
                    # TODO
                    pass
            if len(res) > 0:
                newOffset = res[-1]['update_id']
                self.__db.update_offset(newOffset)
            return True
        else :
            return False

    def parse_message(self, body):
        """Parses messages.
        """
        chat = body['message']['chat']
        chatID = chat['id']
        chatType = chat['type']
        chatDate = body['message']['date']
        if chatType == 'private':
            # Person
            chatFirstName = chat.get('first_name', '')
            chatLastName = chat.get('last_name', '')
            chatUserName = chat.get('username', '')
        else :
            # Group
            chatTitle = chat['title']
        
        messageID = body['message']['message_id']
        messageFrom = body['message']['from']
        messageFromID = messageFrom['id']
        messageFromIsBot = messageFrom['is_bot']
        messageFromLanguageCode = 'TR'
        messageFromFirstName = messageFrom.get('first_name', '')
        messageFromLastName = messageFrom.get('last_name', '')
        messageFromUserName = messageFrom.get('username', '')
        messageFromLanguageCode = messageFrom.get('language_code', 'TR')
        
        content = ""

        if 'text' in body['message']:
            content += "Text: " + body['message']['text'] + " "
        
        if 'photo' in body['message']:
            content += "Photo: " + body['message']['photo'][-1]['file_id'] + " "
            if 'caption' in body['message']:
                content += "Caption: " + body['message']['caption'] + " "

        if 'document' in body['message']:
            content += "File: " + body['message']['document']['file_id'] + " "
            if 'caption' in body['message']:
                content += "Caption: " + body['message']['caption'] + " "
        
        if 'text' in body['message']:
            responses = self.__r.respond(body['message']['text'])

        logText = "Message from: %s %s (%s) - %s - %s - ID: %s" % (messageFromFirstName, messageFromLastName, messageFromUserName, chatDate, content, messageID)
        if chatType != 'private' :
            logText += " - Group: " + chatTitle

        if self.__verbose is True:
            print(logText)
        if self.__logging is True:
            if chatType == 'private': 
                self.__db.log(messageFromID, messageFromFirstName, messageFromLastName, messageFromUserName, messageID, chatDate, content, 0)
            else :
                self.__db.log(messageFromID, messageFromFirstName, messageFromLastName, messageFromUserName, messageID, chatDate, content, chatID, chatTitle)
            # TODO
            # Log responses from the bot

        if responses is not []:
            for m in responses:
                if m == ('service', 1):
                    if self.__db.check_service(messageFromID, 1) is True:
                        self.send_message(chatID, 'Yemekhane servisine zaten abonesiniz.', messageID)
                    else :
                        self.__db.add_service(messageFromID, 1)
                        self.send_message(chatID, 'Yemekhane servisine abone oldunuz.', messageID)
                else :
                    self.send_message(chatID, m, messageID)


    def parse_inline(self, body):
        """Parses inline messages for inline bot functions.
        """
        inline = body['inline_query']
        messageFrom = inline['from']
        messageFromFirstName = messageFrom.get('first_name', '')
        messageFromLastName = messageFrom.get('last_name', '')
        messageFromUserName = messageFrom.get('username', '')
        messageFromLanguageCode = messageFrom.get('language_code', 'TR')
        messageFromID = messageFrom['id']
        messageFromIsBot = messageFrom['is_bot']
        inlineID = inline['id']
        inlineQuery = inline['query']


        # TODO 
        print("Inline")

    def send_inline_response(self, inline_query_id, results):
        # TODO
        url = self.__url + "/answerInlineQuery"
        params = {'inline_query_id': inline_query_id,
                  'results': []}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok'] == True:
            return True
        else :
            return False


    def send_message(self, chat_id, message, reply = 0):
        """Send messages as the bot.
        chat_id -- The chat ID to send the message to
        message -- The message body
        reply   -- If a reply 1, otherwise by default 0
        Returns boolean.
        """
        url = self.__url + "/sendMessage"
        params = {'chat_id': chat_id,
                  'text': message, 
                  'parse_mode': 'Markdown'}
        if reply != 0:
            params['reply_to_message_id'] = reply
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok'] == True:
            return True
        else :
            return False

    def send_service_messages(self):
        """Send service messages as the bot.
        """
        now = datetime.datetime.now()
        clock = (now.hour, now.minute)
        weekdayMorning = {1: self.__r.food}
        if now.weekday() < 5 and clock == (9, 0):
            for key, val in weekdayMorning.items():
                if self.__db.check_if_service_sent_today(key) is False:
                    users = self.__db.get_service_users(key)
                    for i in users:
                        self.send_message(i, val())
                    self.__db.mark_service_sent_today(key)

