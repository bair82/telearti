import os, time
import telebot
from flask import Flask, request
import langchaintest, poe
from notion_client import Client

NOTION_KEY = os.environ["NOTION_KEY"]
notion = Client(auth=NOTION_KEY)
db_id = "c2891605-abc6-457c-8125-baaf93b6ce61"

BOT_TOKEN = os.environ.get('BOT_TOKEN')


URL = "https://telearti.onrender.com/"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

message_history = []

def add_todo_task(task):
    try:
        new_page = {
          "Name": {
        "title": [{
          "type": "text",
          "text": {
            "content": f"{task}"
          }
        }]
      },
      "Status": {
        "select": {
          "id": '1'
        }
      }
    }
        result = notion.pages.create(parent={"database_id": db_id},
                             properties=new_page)
    except:
        print("Error")
        

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['todo'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, action="typing")
    if message.message_id not in message_history:
        message_history.append(message.message_id)
        add_todo_task(message.text.lstrip("/todo".strip()))
        bot.reply_to(message, "Task added!")
        if len(message_history) > 50:
            message_history.pop(0)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_chat_action(message.chat.id, action="typing")
    if message.message_id not in message_history:
        message_history.append(message.message_id)
        #text = langchaintest.reply(message.text)
        text = poetest.reply(message.text)
        bot.reply_to(message, text)
        if len(message_history) > 50:
            message_history.pop(0)

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
