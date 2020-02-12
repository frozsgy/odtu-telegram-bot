from responses import Responses
from db import DB

import requests
import json

class Bot():
    """Class for handling all communication with the Telegram API. 

    Attributes:
        _url -- the url for Telegram Bot API
        _debug -- if on, logging will be active
    """

    # https://api.telegram.org/bot<token>/METHOD_NAME
    _url = "https://api.telegram.org/bot"
    _debug = False
    _token = ""

    def __init__(self, debug = False):
        self._db = DB()
        self._token = self._db.getToken()
        self._url += self._token
        self._r = Responses()
        self._debug = debug

    def hello(self):
        """Tester method to check if the bot class works properly.
        """
        print("Hello, I am running nicely.")

    def getUpdates(self):
        """Gets updates from the Telegram Server. Uses Long Polling.
        Returns boolean.
        """
        url = self._url + "/getUpdates"
        offset = self._db.getOffset()
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
                    self.parseMessage(i)                    
                elif 'inline_query' in i:
                    self.parseInline(i)
                else :
                    # TODO
                    pass
            if len(res) > 0:
                newOffset = res[-1]['update_id']
                self._db.updateOffset(newOffset)
            return True
        else :
            return False

    def parseMessage(self, body):
        """Parses messages.
        """
        chat = body['message']['chat']
        chatID = chat['id']
        chatType = chat['type']
        if chatType == 'private':
            #person
            try:
                chatFirstName = chat['first_name']
            except:
                chatFirstName = None
            try:
                chatLastName = chat['last_name']
            except:
                chatLastName = None
            try:
                chatUserName = chat['username']
            except:
                chatUserName = None
        else :
            #group
            chatTitle = chat['title']
        chatDate = body['message']['date']
        messageID = body['message']['message_id']
        messageFrom = body['message']['from']
        try:
            messageFromFirstName = messageFrom['first_name']
        except:
            messageFromFirstName = None
        try:
            messageFromLastName = messageFrom['last_name']
        except:
            messageFromLastName = None
        try:
            messageFromUserName = messageFrom['username']
        except:
            messageFromUserName = None
        messageFromID = messageFrom['id']
        messageFromIsBot = messageFrom['is_bot']
        try:
            messageFromLanguageCode = messageFrom['language_code']
        except:
            messageFromLanguageCode = "TR"
        content = ""
        if 'text' in body['message']:
            content += "Text: " + body['message']['text'] + " "
        if 'photo' in body['message']:
            content += "Caption: " + body['message']['caption'] + " "
            content += "Photo: " + body['message']['photo'][-1]['file_id']
        if 'document' in body['message']:
            content += "Caption: " + body['message']['caption'] + " "
            content += "File: " + body['message']['document']['file_id']

        responses = self._r.respond(content)

        if self._debug is True:
            logText = "Message from: %s %s (%s) - %s - %s - ID: %s" % (messageFromFirstName, messageFromLastName, messageFromUserName, chatDate, content, messageID)
            if chatType != 'private' :
                logText += " - Group: " + chatTitle
            print(logText)
            if chatType == 'private': 
                self._db.log(messageFromID, messageFromFirstName, messageFromLastName, messageFromUserName, messageID, chatDate, content, 0)
            else :
                self._db.log(messageFromID, messageFromFirstName, messageFromLastName, messageFromUserName, messageID, chatDate, content, chatID, chatTitle)
            # TODO
            # Log responses from the bot

        if responses is not []:
            for m in responses:
                self.sendMessage(chatID, m, messageID)


    def parseInline(self, body):
        """Parses inline messages for inline bot functions.
        """
        inline = body['inline_query']
        messageFrom = inline['from']
        messageFromFirstName = messageFrom['first_name']
        messageFromLastName = messageFrom['last_name']
        try:
            messageFromUserName = messageFrom['username']
        except:
            messageFromUserName = None
        messageFromID = messageFrom['id']
        messageFromIsBot = messageFrom['is_bot']
        try:
            messageFromLanguageCode = messageFrom['language_code']
        except:
            messageFromLanguageCode = "TR"
        inlineID = inline['id']
        inlineQuery = inline['query']


        # TODO 
        print("Inline")

    def sendInlineResponse(self, inline_query_id, results):
        # TODO
        url = self._url + "/answerInlineQuery"
        params = {'inline_query_id': inline_query_id,
                  'results': []}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok'] == True:
            return True
        else :
            return False


    def sendMessage(self, chat_id, message, reply = 0):
        """Send messages as the bot.
        chat_id -- The chat ID to send the message to
        message -- The message body
        reply   -- If a reply 1, otherwise by default 0
        Returns boolean.
        """
        url = self._url + "/sendMessage"
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


