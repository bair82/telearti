from poe import load_chat_id_map, clear_context, send_message, get_latest_message, set_auth
import os

FK = os.environ["FORMKEY"]
CK = os.environ["COOKIE"]
#Auth
set_auth('Quora-Formkey',FK)
set_auth('Cookie','m-b='+CK)
bot = 'a2'

chat_id = load_chat_id_map(bot)
#clear_context(chat_id)

def reply(message):
  send_message(message,bot,chat_id)
  reply = get_latest_message(bot)
  return reply
