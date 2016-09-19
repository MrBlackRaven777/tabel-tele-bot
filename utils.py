'''
Created on 14 сент. 2016 г.

@author: voskresenskiy
'''
import shelve
from SQLighter import SQLighter
from config_bot import shelve_name
def user_came(user_id):
    with shelve.open(shelve_name) as storage:
        storage[str(user_id)] = 