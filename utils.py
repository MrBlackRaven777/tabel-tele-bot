'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
from PostGreSQL import PostGreSQL
from config_bot import database_name
from _datetime import datetime as dt, timedelta
from time import strptime
import os

def time_count(user_id,strdate):
    dbw = PostGreSQL(database_name)
    try:
        all_time = "".join(dbw.read(user_id,strdate))
        if len(all_time)>0:
            times = all_time.split('-')
            if len(times)%2==0:
                sum_time=[]
                for i in range(0,len(times),2):
                    t1=dt.strptime(times[i],"%H:%M")
                    t2=dt.strptime(times[i+1],"%H:%M")
                    sum_time.append(t2-t1)
                summ = sum(sum_time,timedelta())
                str_summ = str(summ)[:-3]
                dt_summ = dt.strptime(str_summ,"%H:%M")
                if dt_summ.minute > 14 and dt_summ.minute < 45:
                    end_summ_hour = dt_summ.hour
                    end_summ_min = 30
                elif dt_summ.minute > 44:
                    end_summ_min = "00"
                    end_summ_hour = dt_summ.hour + 1
                elif dt_summ.minute < 15:
                    end_summ_hour = dt_summ.hour
                    end_summ_min = "00"
                return str(end_summ_hour) + ":" + str(end_summ_min)
            else:
                return "Вы еще в офисе."
        else:
            return "Вы не были на работе в указанную дату: "+strdate
    except:
        return "Что-то пошло не так (ошибка 4)"
    
def user_came(user_id):
    dbw = PostGreSQL()
    dbw.check_user(user_id)
    onWork = dbw.read(user_id,"onWork") 
    if onWork[0] == "True":
        return "Вы уже на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже(ошибка 1)"
    elif onWork[0] == "False" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        dbw.upd(user_id,onWork="True",timeOn=time)
        return "Вы пришили в {}".format(time)
    else:
        return "Чето не так(ошибка 3)"
    dbw.close()
    
def user_left(user_id):
    dbw = PostGreSQL()
    dbw.check_user(user_id)
    onWork = dbw.read(user_id,"onWork") 
    nowdate = dt.strftime(dt.now(), "%Y.%m.%d")
    if onWork[0] == "False":
        return "Вы еще не на работе"
    elif onWork == None:
        return "Not in base"
    elif onWork[0] == "Err":
        return "Происзошла какая-то ошибка. Попробуйте позже"
    elif onWork[0] == "True" or "empty":
        time = dt.strftime(dt.now(), "%H:%M")
        dbw.upd(user_id,onWork="False",timeOn=time)
        work_time = time_count(user_id, nowdate)
        work_time_number = int(dt.strptime(work_time,"%H:%M").hour) +  int(dt.strptime(work_time,"%H:%M").minute)/60
        stavka = dbw.read(user_id,"stavka")
        return "Вы ушли в {0}. Общее время работы: {1}. Общий заработок за сегодня: {3}".format(time, work_time,work_time, work_time_number * int(stavka[0]))
    else:
        return "Чето не так(ошибка 2)"
    dbw.close()