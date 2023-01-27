import os, time
import telebot
from flask import Flask, request
import langchaintest

BOT_TOKEN = os.environ.get('BOT_TOKEN')
#headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}

URL = "https://telearti.onrender.com/"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_chat_action(message.chat.id, action="typing")
    #time.sleep(5)
    text = reply(message.text)
    bot.reply_to(message, text)

# Webhook
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + BOT_TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
