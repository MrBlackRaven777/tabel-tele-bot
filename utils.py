'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
from SQLighter import SQLighter
from config_bot import database_name
from _datetime import datetime as dt

def user_came(user_id):
    db = SQLighter(database_name)
    onWork = db.read(user_id,"onWork") 
    if onWork == "True":
        return("Вы уже на работе")
    elif onWork == None:
        return "Not in base"
    elif onWork == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork == "False":
        db.upd(user_id,onWork="True",timeOn=dt.strftime(dt.now(), "%H:%M"))
        return("Вы пришили в {}".format(dt.strftime(dt.now(), "%H:%M"))