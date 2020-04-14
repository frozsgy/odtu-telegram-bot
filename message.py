
class TelegramMessage:

    has_text = False
    has_attachment = False
    text = ""
    attachment = ""
    content = ""

    def __init__(self, body):
        message = body['message']
        chat = message['chat']
        self.chat_id = chat['id']
        self.chat_type = chat['type']
        self.chat_date = message['date']
        if self.chat_type == 'private':
            # Person
            self.chat_first_name = chat.get('first_name', '')
            self.chat_last_name = chat.get('last_name', '')
            self.chat_user_name = chat.get('username', '')
        else :
            # Group
            self.chat_title = chat['title']
        
        self.message_id = message['message_id']
        message_from = message['from']
        self.message_from_id = message_from['id']
        self.message_from_is_bot = message_from['is_bot']
        self.message_from_language_code = 'TR'
        self.message_from_first_name = message_from.get('first_name', '')
        self.message_from_last_name = message_from.get('last_name', '')
        self.message_from_user_name = message_from.get('username', '')
        self.message_from_language_code = message_from.get('language_code', 'TR')
        
        
        if 'text' in message:
            self.text = message['text']
            self.has_text = True
        elif 'caption' in message:
            self.text = message['caption']
            self.has_text = True

        if 'photo' in message:
            self.attachment = message['photo'][-1]['file_id']
            self.has_attachment = True
            self.attachment_type = "Photo"  
        elif 'document' in message:
            self.attachment = message['document']['file_id']
            self.has_attachment = True
            self.attachment_type = "File"

        content_title = "Caption: " if self.has_attachment else "Text: "
        content_title += self.text + " "

        if self.has_attachment:
            self.content = self.attachment_type + ": " + self.attachment + " "
        if self.text != "":
            self.content += content_title


    def generate_log_text(self):
        log_text = "Message from: %s %s (%s) - %s - %s - ID: %s" % (self.message_from_first_name, self.message_from_last_name, self.message_from_user_name, self.chat_date, self.content, self.message_id)
        if self.chat_type != 'private' :
            log_text += " - Group: " + self.chat_title
        return log_text       

    def generate_log_tuple(self):
        log_chat_id = 0 if self.chat_type == 'private' else self.chat_id
        log_chat_title = 'private' if self.chat_type == 'private' else self.chat_title
        return (self.message_from_id, self.message_from_first_name, self.message_from_last_name, self.message_from_user_name, self.message_id, self.chat_date, self.content, log_chat_id, log_chat_title)

        