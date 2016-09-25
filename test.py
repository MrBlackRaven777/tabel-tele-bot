import sqlite3
from SQLighter import SQLighter as SQLi
import config_bot
from datetime import datetime as dt, timedelta
import time
import utils
dbw = SQLi(config_bot.database_name)

utils.time_count(33261,'2016.09.25')