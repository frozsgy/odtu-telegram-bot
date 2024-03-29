import datetime
import json

import requests

from db import DB
from logger import logger
from message import TelegramMessage
from responses import Responses


class Bot:
    """Class for handling all communication with the Telegram API. 

    Attributes:
        __url -- the url for Telegram Bot API
    """

    # https://api.telegram.org/bot<token>/METHOD_NAME
    __url = "https://api.telegram.org/bot"

    def __init__(self, logging_enabled=False):
        self.__db = DB()
        self.__token = self.__db.get_token()
        self.__url += self.__token
        self.__r = Responses()
        self.__logging = logging_enabled

    def hello(self):
        """Tester method to check if the bot class works properly.
        """
        logger.info("Hello, I am running nicely.")

    def get_updates(self):
        """Gets updates from the Telegram Server. Uses Long Polling.
        Returns boolean.
        """
        url = self.__url + "/getUpdates"
        offset = self.__db.get_offset()
        params = {
            'offset': int(offset) + 1,
            'limit': 100,
            'timeout': 0,
            'allowed_updates': ['message']
        }
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
                else:
                    # TODO
                    pass
            if len(res) > 0:
                new_offset = res[-1]['update_id']
                self.__db.update_offset(new_offset)
            return True
        else:
            return False

    def get_file(self, file_id):
        """Gets files from the Telegram Server.
        Returns boolean.
        """
        url = self.__url + "/getFile"
        params = {'file_id': file_id}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok'] is True:
            res = items['result']
            file_path = res['file_path']
            url = "https://api.telegram.org/file/bot" + self.__token + "/" + file_path
            # TODO - to handle file processing
            # logger.info(url + file_path)
            return True
        else:
            return False

    def parse_message(self, body):
        """Generates a TelegramMessage object from the message.
        """
        user_message = TelegramMessage(body.get('message'))
        responses = self.__r.respond(user_message.text) if user_message.has_text else []
        log_text = user_message.generate_log_text()

        logger.debug(log_text)
        if self.__logging is True:
            self.__db.log(*user_message.generate_log_tuple())

        sent_message = self.respond_to_message(user_message, responses)

        if self.__logging is True:
            for m in sent_message:
                bot_response = TelegramMessage(m)
                self.__db.log(*bot_response.generate_log_tuple())

    def respond_to_message(self, tm, responses):
        """Sends responses to the messages.
        """
        sent_responses = []
        for m in responses:
            if m == ('service', 1):
                if self.__db.check_service(tm.message_from_id, 1) is True:
                    self.__db.remove_service(tm.message_from_id, 1)
                    sent_responses.append(
                        self.send_message(tm.chat_id, 'Yemekhane servisi aboneliğiniz sonlandırıldı.', tm.message_id)
                    )
                else:
                    self.__db.add_service(tm.message_from_id, 1)
                    sent_responses.append(
                        self.send_message(tm.chat_id, 'Yemekhane servisine abone oldunuz.', tm.message_id)
                    )
            else:
                sent_responses.append(self.send_message(tm.chat_id, m, tm.message_id))
        return sent_responses

    def parse_inline(self, body):
        """Parses inline messages for inline bot functions.
        """
        inline = body['inline_query']
        message_from = inline['from']
        message_from_first_name = message_from.get('first_name', '')
        message_from_last_name = message_from.get('last_name', '')
        message_from_user_name = message_from.get('username', '')
        message_from_language_code = message_from.get('language_code', 'TR')
        message_from_id = message_from['id']
        message_from_is_bot = message_from['is_bot']
        inline_id = inline['id']
        inline_query = inline['query']

        # TODO
        logger.debug("Inline")

    def send_inline_response(self, inline_query_id, results):
        # TODO
        url = self.__url + "/answerInlineQuery"
        params = {'inline_query_id': inline_query_id, 'results': []}
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok']:
            return True
        else:
            return False

    def send_message(self, chat_id, message, reply=0):
        """Send messages as the bot.
        chat_id -- The chat ID to send the message to
        message -- The message body
        reply   -- If a reply 1, otherwise by default 0
        Returns result if successful, False otherwise.
        """
        url = self.__url + "/sendMessage"
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        if reply != 0:
            params['reply_to_message_id'] = reply
        r = requests.post(url, params)
        page = r.content
        items = json.loads(page)
        if items['ok']:
            return items.get('result')
        else:
            return False

    def send_service_messages(self):
        """Send service messages as the bot.
        """
        now = datetime.datetime.now()
        clock = (now.hour, now.minute)
        weekday_morning = {1: self.__r.food}
        if now.weekday() < 5 and clock == (9, 0):
            for key, val in weekday_morning.items():
                if self.__db.check_if_service_sent_today(key) is False:
                    users = self.__db.get_service_users(key)
                    for i in users:
                        self.send_message(i, val())
                    self.__db.mark_service_sent_today(key)
