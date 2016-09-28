import psycopg2
from PostGreSQL import PostGreSQL as SQLi
import config_bot
from datetime import datetime as dt, timedelta
import time
import utils
import os
#dbw = SQLi(config_bot.database_name)

#utils.time_count(332761,'2016.09.25')
print(SQLi().get_columns())
print(SQLi().check_date())
#print( os.path.dirname(os.path.abspath(__file__)))