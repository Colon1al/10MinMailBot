import sys
sys.path.append(r"C:\Users\HyperX\Desktop\RandomPython\10MinMailBot\10MinMailBot")

import flask
import secrets, string
import time as tm
import collections
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from sql_lib.postgresql import database


token = "2129777308:AAG-d5t3jdTbKapQqHHfEmPgFiamh7I1WDY"
host = "somerandomserver.xyz"
port = 8443
listen = "0.0.0.0"
crt = ""
key = ""

webhook_url_base = f"https://{host}:{port}"
webhook_url_path = f"/{token}/"

app = flask.Flask(__name__)
 

class MailBot(object):

    def __init__(self, token):
        self.updater = Updater(token=token)  # заводим апдейтера
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)  # ставим обработчик всех текстовых сообщений
        self.handlers_map = {"mailbox": collections.defaultdict(self.mail_dialog),
                        "password": collections.defaultdict(self.password_dialog),} # заводим мапу "id чата -> генератор"
        self.db = database(r"sql_lib\test_db.db")

    def start(self):
        self.updater.start_polling()

    def handle_message(self, update, context):
        print("Received", update.message)
        chat_id = update.message.chat_id
        answer = "Попробуйте снова" 
        if update.message.text == "/start":
            # если передана команда /start, начинаем всё с начала
            for handlers in self.handlers_map.values():
                handlers.pop(chat_id, None)
            
            if not self.db.doesUserExist(chat_id):
                self.db.writeNewUserData(chat_id, update.message.chat.first_name, update.message.chat.last_name)
            answer = "Добавить сюда инструкцию" #TODO Instruction
        for handlers in self.handlers_map.values():
            if chat_id in handlers:
                print(chat_id)
                # если диалог уже начат, то надо использовать .send(), чтобы
                # передать в генератор ответ пользователя
                try:
                    answer = handlers[chat_id].send(update.message)
                except StopIteration:
                    # если при этом генератор закончился -- что делать, начинаем общение с начала
                    del handlers[chat_id]
                    # (повторно вызванный, этот метод будет думать, что пользователь с нами впервые)
                    return self.handle_message(update, context)

        if update.message.text == "/new_mailbox":
            #create new mailbox
            #send mail data to user
            mailbox = "test@test.test"
            answer = f"Почтовый ящик: {mailbox}" 


        elif update.message.text == "/password":
            answer = next(self.handlers_map["password"][chat_id])

        context.bot.sendMessage(chat_id=chat_id, text=answer)

    def password_dialog(self):
        answer = yield "Укажите идентификатор пароля"
        service = answer.text.rstrip(".!")
        alphabet = string.ascii_letters + string.digits + "!#$%^&*_-"
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        self.db.writeUserServiceData(answer.chat_id, service, password)
        answer = yield f"{service} : {password}"

    def mail_dialog(self):
        answer = yield "MAIL Здравствуйте! Меня забыли наградить именем, а как зовут вас?"
        name = answer.text.rstrip(".!").split()[0].capitalize()
        answer = yield f"MAIL Приятно познакомиться, {name}. Вам нравится Питон?"

if __name__=="__main__":
    mail_bot = MailBot(token)
    mail_bot.start()
    