'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
from SQLighter import SQLighter
from config_bot import database_name
from _datetime import datetime as dt, timedelta
from time import strptime
import os

def time_count(user_id,date):
    dbw = SQLighter(database_name)
    try:
        all_time = str(dbw.read(user_id,'"'+date+'"')[0])
        print(all_time)
        if len(all_time)>0:
            times = all_time.split('-')
            print(times)
            if len(times)%2==0:
                sum_time=[]
                for i in range(0,len(times),2):
                    
                    t1=dt.strptime(times[i],"%H:%M")
                    t2=dt.strptime(times[i+1],"%H:%M")
                    print(t1)
                    print(t2)
                    print(t2-t1)
                    sum_time.append(t2-t1)
                    print(sum(sum_time))
            #else:
                #return "Вы еще в офисе"
    except:
        pass
    
def user_came(user_id):
    dbw = SQLighter(database_name)
    dbw.check_user(user_id)
    onWork = dbw.read(user_id,"onWork") 
    if onWork[0] == "True":
        return "Вы уже на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork[0] == "False" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        dbw.upd(user_id,onWork="True",timeOn=time)
        return "Вы пришили в {}".format(time)
    else:
        return "Чето не так"
    dbw.close()
    
def user_left(user_id):
    dbw = SQLighter(database_name)
    dbw.check_user(user_id)
    onWork = dbw.read(user_id,"onWork") 
    if onWork[0] == "False":
        return "Вы еще не на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork[0] == "True" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        dbw.upd(user_id,onWork="False",timeOn=time)
        return "Вы ушли в {}".format(time)
    else:
        return "Чето не так"
    dbw.close()