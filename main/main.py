import telebot, flask
import secrets
import time as tm

token = ""
host = ""
port = 8443
listen = ""
crt = ""
key = ""

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
keybrd.row("", "", "")


@bot.message_handler(commands=['start'])
def start_message(message):
	pass

@bot.message_handler(content_types=['text'])
def send_text(message):
	pass



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