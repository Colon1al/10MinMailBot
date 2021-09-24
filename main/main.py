import telebot, flask
import secrets
import time as tm
gachiSongs = ["https://www.youtube.com/watch?v=aiEJgyGUwIk",
"https://www.youtube.com/watch?v=1YS6js8uzZE",
"https://www.youtube.com/watch?v=SVHj64ltMb8",
"https://www.youtube.com/watch?v=NLq6KtlwnRA",
"https://www.youtube.com/watch?v=eKHwSCHpij8",
"https://www.youtube.com/watch?v=7Yd_Sd7ATKk"]

AnimeSongs = ["https://www.youtube.com/watch?v=woFU8DGg1UI",
"https://www.youtube.com/watch?v=hsfBOwAIhOw",
"https://www.youtube.com/watch?v=fqBNnC_apV4",
"https://www.youtube.com/watch?v=HYNK0YRqZb4",
"https://www.youtube.com/watch?v=-77UEct0cZM",
"https://www.youtube.com/watch?v=2Od7QCsyqkE",
"https://www.youtube.com/watch?v=0Vwwr3VGsYg",
"https://www.youtube.com/watch?v=3uHGkJbNkX0",]


lucky = ["https://www.youtube.com/watch?v=woFU8DGg1UI",
"https://www.youtube.com/watch?v=hsfBOwAIhOw",
"https://www.youtube.com/watch?v=fqBNnC_apV4",
"https://www.youtube.com/watch?v=HYNK0YRqZb4",
"https://www.youtube.com/watch?v=-77UEct0cZM",
"https://www.youtube.com/watch?v=2Od7QCsyqkE",
"https://www.youtube.com/watch?v=0Vwwr3VGsYg",
"https://www.youtube.com/watch?v=3uHGkJbNkX0",
"https://www.youtube.com/watch?v=aiEJgyGUwIk",
"https://www.youtube.com/watch?v=1YS6js8uzZE",
"https://www.youtube.com/watch?v=SVHj64ltMb8",
"https://www.youtube.com/watch?v=NLq6KtlwnRA",
"https://www.youtube.com/watch?v=eKHwSCHpij8",
"https://www.youtube.com/watch?v=7Yd_Sd7ATKk"
]

stickers=["CAACAgIAAxkBAAEBu6Nf7P0_t0oAAQKxuRKuA16fR1JqrboAAkEAAzyKVxogmx2BPCogYB4E",
"CAACAgIAAxkBAAEBu6Vf7P1kcpN7qv92_f1n55XJT-4r2wACcAADPIpXGsTfmCv8KFvZHgQ",
"CAACAgIAAxkBAAEBu6df7P1wdq0TcBFVEnv-iBGmh46q4QAC6wADPIpXGlHmsiTHWML5HgQ",
"CAACAgIAAxkBAAEBu6lf7P19Ogd0KbvCXy_CanP1BrniSQACwwADPIpXGl-TK5yudYfXHgQ",
"CAACAgIAAxkBAAEBu6tf7P2ILBTa0W4gmfmAhBE0LjppmAAC9AADPIpXGidgfMebbIuVHgQ",
"CAACAgIAAxkBAAEBu69f7P2W7OFByLRaZ4Xj9pnKn0e53AACBQEAAjyKVxrKuyM_Svr6jh4E",
"CAACAgIAAxkBAAEBu7Ff7P2lMhvPkRoawGdHcXfC2Mu6AAMiAQACJYbKBP8P_E-Y1P9kHgQ",
"CAACAgIAAxkBAAEBu7Nf7P2u6wZuY2nZnxnmGs6HkckuigACJAEAAiWGygQt6s4ZBKkPyh4E",
"CAACAgIAAxkBAAEBu7Vf7P3JPGT3-cnh8IgyId-1ZP_S7wACNwEAAiWGygSEb81q97q2xx4E",
"CAACAgIAAxkBAAEBu7df7P3bgYMTZr7S_s_qMdsTlVBVggACUgEAAiWGygRclUejJKQlJx4E",
"CAACAgQAAxkBAAEBu7lf7P3uR_wTVjrr4BDVoGCzA1Af6gACzDQAAuOnXQUBf0rQMBlr_R4E",
"CAACAgQAAxkBAAEBu71f7P4k8ussim-6qlMuHVeNqAVElgAC7DQAAuOnXQUhqa38LsZxSh4E",
"CAACAgUAAxkBAAEBu8Ff7P5PiDT0vwxn2qBDlUpDxrHwIwACRgADDGCzCASlAlZol2PsHgQ",
"CAACAgIAAxkBAAEBu8Nf7P5aNSx3fcv2u_1fFAABRqjOTVwAAg0AAzlKsg0ehxmvTYKBHR4E",
"CAACAgIAAxkBAAEBu8Vf7P5eQ8ofiYClevouiRlbn_mksgACEAADOUqyDculAAEorbaDXB4E",
"CAACAgIAAxkBAAEBu8df7P53RZd2nssqI-A6K-qT5TeGuQACIQADOUqyDYzGwN4FhGsoHgQ",
"CAACAgIAAxkBAAEBu8lf7P6N74zvoOTHyhTODOMUzW78HgACBAYAAo-dWgVTYTHNewobmB4E",
"CAACAgIAAxkBAAEBu8tf7P6mCT_22MAB-t0Ot-m6XQcdxgAC5wUAAo-dWgWP5zAfHsaMpx4E",
"CAACAgUAAxkBAAEBu79f7P496TbRnk5l5PWfupR83NNbbgACXwADDGCzCCtBNT3iQF2NHgQ"
]


token = ""
host = "somerandomserver.xyz"
port = 8443
listen = "0.0.0.0"
crt = "/root/crt/webhook_cert.pem"
key = "/root/crt/webhook_pkey.pem"

webhook_url_base = f"https://{host}:{port}"
webhook_url_path = f"/{token}/"

app = flask.Flask(__name__)

# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@app.route(webhook_url_path, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)



bot = telebot.TeleBot(token)

keybrd = telebot.types.ReplyKeyboardMarkup(True)
keybrd.row("GachiBASS", "Anime Song", "I am lucky")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEBu7tf7P36CFVlTr4saZanezFf8UtttgACzTQAAuOnXQWA2ep6IWeNtR4E" ,reply_markup=keybrd)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'gachibass':
        bot.send_sticker(message.chat.id, secrets.choice(stickers))
        bot.send_message(message.chat.id, f"Ass with me BOOOY -> {secrets.choice(gachiSongs)}" ,reply_markup=keybrd)
        
    elif message.text.lower() == 'anime song':
        bot.send_sticker(message.chat.id, secrets.choice(stickers))
        bot.send_message(message.chat.id, f"Hello bruda -> {secrets.choice(AnimeSongs)}" ,reply_markup=keybrd)
        
    elif message.text.lower() == 'i am lucky':
        bot.send_sticker(message.chat.id, secrets.choice(stickers))
        bot.send_message(message.chat.id, f'YEET -> {secrets.choice(lucky)}' ,reply_markup=keybrd)
        

bot.remove_webhook()

tm.sleep(0.1)

# Set webhook
bot.set_webhook(url=webhook_url_base + webhook_url_path,
                certificate=open(crt, 'r'))

# Start flask server
app.run(host=listen,
        port=port,
        ssl_context=(crt, key),
        debug=True)