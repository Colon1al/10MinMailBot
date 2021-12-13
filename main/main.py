import sys
sys.path.append(r"C:\Users\HyperX\Desktop\RandomPython\10MinMailBot\10MinMailBot")

import flask
import secrets, string
import time as tm
import collections
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram import ReplyKeyboardMarkup
from sql_lib.postgresql import database
from mail_service.dropmail import mail_handler
from datetime import datetime as dt, timedelta

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
        custom_keyboard = [['/password', '/all_passwords', '/new_mailbox', '/check_mail']]
        self.reply_markup = ReplyKeyboardMarkup(custom_keyboard)

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
            answer = """Вы можете создать временный почтовый ящик через /new_mailbox \n
            Проверить активный почтовый ящик через /check_mail\n
            Создать новый пароль можно через /password\n
            Показать все сохраненные пароли /all_passwords """ #TODO Instruction
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
            self.db.removeMailbox(chat_id)
            mail = mail_handler(chat_id)
            mailbox_data = mail.new_mailbox()
            mailbox_name = mailbox_data["introduceSession"]["addresses"][0]["address"]
            self.db.writeNewMailboxData(
                chat_id,
                mailbox_data["introduceSession"]["id"],
                mailbox_name)
            #send mail data to user
            answer = f"Почтовый ящик: {mailbox_name}, истекает {dt.now().__add__(timedelta(minutes=10)).strftime('%H:%M:%S %Y-%m-%d')}" 

        if update.message.text == "/check_mail":
            mailbox = self.db.getMailboxData(chat_id)
            mail = mail_handler(chat_id, mailbox[0][1])
            mail_letters = mail.get_mail() 
            letters = []
            if mail_letters["session"] :
                if mail_letters['session']['mails']:
                    for letter in mail_letters["session"]["mails"]:
                        letter_formatted = f"От: {letter['fromAddr']} \n \nТема: {letter['headerSubject']} \n{letter['text']}"
                        letters.append(letter_formatted) 
                    answer = letters 
                else: answer = "Почтовый ящик пуст"
            else: answer = "Почтовый ящик пуст"

        elif update.message.text == "/password":
            answer = next(self.handlers_map["password"][chat_id])
        
        elif update.message.text == "/all_passwords":
            answer = "\n".join([" : ".join([elem[0],elem[1]]) for elem in self.db.getAllUserPasswords(chat_id)])
            
        if type(answer) is list:
            for elem in answer:
                context.bot.sendMessage(chat_id=chat_id, text=elem, reply_markup=self.reply_markup)
        else: context.bot.sendMessage(chat_id=chat_id, text=answer, reply_markup=self.reply_markup) 

    def password_dialog(self):
        answer = yield "Укажите идентификатор пароля"
        service = answer.text.rstrip(".!")
        alphabet = string.ascii_letters + string.digits + "!#$%^&*_-"
        password = ''.join(secrets.choice(alphabet) for i in range(12))
        self.db.writeUserServiceData(answer.chat_id, service, password)
        answer = yield f"{service} : {password}"

    def mail_dialog(self): pass

if __name__=="__main__":
    mail_bot = MailBot(token)
    mail_bot.start()
    