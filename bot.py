'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
import config_bot
import telebot
import utils

bot = telebot.TeleBot(config_bot.token)
    
@bot.message_handler(content_type=['text'])       
def repeart(message):
    bot.send_message(message.chat.id,message.chat.id)
	
@bot.message_handler(commands=['came'])   
def user_came(message):
    bot.send_message(message.chat.id,utils.user_came(message.chat.id))
    
@bot.message_handler(commands=['left'])
def user_left(message):
    bot.send_message(message.chat.id, utils.user_left(message.chat.id))

@bot.message_handler(commands=['info'])
def user_info(message):
    pass
    #SQLig.check_user(message.chat.id)
    
if __name__ == '__main__':
    bot.polling(none_stop=True)