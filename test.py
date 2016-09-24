import sqlite3
from SQLighter import SQLighter as SQLi
import config_bot
from datetime import datetime as dt
import time
dbw = SQLi(config_bot.database_name)
#column = input("Введите название колонки: ")
#user_id = input("Введите ID: ")
#print(dbw.read(user_id,column))
nowtime = dt.today()
print(dt.strftime(dt.now(), "%H:%M"))
print(dbw.check_date())
print(dbw.add(445566,stavka=220,onWork="False"))
#nowtime1 = str(nowtime).split(".")#time.strptime(str(nowtime), "%Y-%m-%d %X")
#print(nowtime1)
#nowtime = time.strftime("%H:%M:%S",nowtime1[0])
#print(nowtime)