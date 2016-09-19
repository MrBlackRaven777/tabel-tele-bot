'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
import config_bot
import telebot
from SQLighter import SQLighter as SQLig

bot = telebot.TeleBot(config_bot.token)

@bot.message_handler(content_types=["text"])
#def repeart_all_messages(message):
#    bot.send_message(message.chat.id, message.chat.id)
#
def check_db(message):
    db_worker = SQLig(config_bot.database_name)
    a = db_worker.select_single(message.chat.id)
    bot.send_message(message.chat.id, a)
    #print(a)
    db_worker.close()
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)