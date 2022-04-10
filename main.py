import os
import telebot
from App import App

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

ab = False
dt =  False
gm = False

@bot.message_handler(commands=['artificial_basis'])
def artificial_basis(message):
  global ab 
  global dt
  global gm
  ab = True
  dt = False
  gm = False
  bot.send_message(message.chat.id, "Task: Artificial basis")
  

@bot.message_handler(commands=['dual_task'])
def dual_task(message):
  global ab 
  global dt
  global gm
  ab = False
  dt = True
  gm = False
  bot.send_message(message.chat.id, "Task: Dual task")

@bot.message_handler(commands=['gomori'])
def gomori(message):
  global ab 
  global dt
  global gm
  ab = False
  dt = False
  gm = True
  bot.send_message(message.chat.id, "Task: Gomori method")

@bot.message_handler(commands=['reset'])
def reset(message):
  global ab 
  global dt
  global gm
  ab = False
  dt =  False
  gm = False
  bot.send_message(message.chat.id, "Reset")

@bot.message_handler(content_types=['text'])
def get_buffer(message):
  global ab 
  global dt
  global gm
  if not (ab or dt or gm):
    bot.send_message(message.chat.id, "Denied")
  else:
    app = App()
    is_okay = app.enter_from_message(message.text)
    if is_okay:
      app.print_to_file()
    else:
      bot.send_message(message.chat.id, "Error")
      return
    if ab:
      app.do_artificial_basis(False)
    elif dt:
      app.do_dual_task(False)
    else:
      app.do_gomori(False)
    file = open('answer.txt', 'rb')
    bot.send_document(message.chat.id, file)
    file.close()

        
bot.polling()
