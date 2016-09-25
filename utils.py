'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
from SQLighter import SQLighter
from config_bot import database_name
from _datetime import datetime as dt

def user_came(user_id):
    db = SQLighter(database_name)
    db.check_user(user_id)
    onWork = db.read(user_id,"onWork") 
    if onWork[0] == "True":
        return "Вы уже на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork[0] == "False" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        db.upd(user_id,onWork="True",timeOn=time)
        return "Вы пришили в {}".format(time)
    else:
        return "Чето не так"
    
def user_left(user_id):
    db = SQLighter(database_name)
    db.check_user(user_id)
    onWork = db.read(user_id,"onWork") 
    if onWork[0] == "False":
        return "Вы еще не на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork[0] == "True" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        db.upd(user_id,onWork="False",timeOn=time)
        return "Вы ушли в {}".format(time)
    else:
        return "Чето не так"