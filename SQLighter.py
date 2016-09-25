import sqlite3
from _sqlite3 import OperationalError
from datetime import datetime as dt

class SQLighter:
    
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_single(self, user_id):
        """ Получаем одну строку с нужным нам id """
        with self.connection:
            tr = self.cursor.execute('SELECT * FROM Tabel WHERE id = ?', (user_id,)).fetchone()
            if tr == []:
                self.cursor.execute('INSERT INTO Tabel VALUES (?,?,?,?)', (user_id,"150","false",""))
                self.connection.commit()
                return "You have been added"
            else:
                return "Your id is {}".format(tr[0])
            
    def get_columns(self):
        try:
            return self.cursor.execute("pragma table_info(Tabel)").fetchall()
        except:
            return false

    def check_user(self,user_id):
        usr = self.connection.execute('SELECT * FROM Tabel WHERE id=?',(user_id,)).fetchone()
        if usr == None:
            self.add(user_id,stavka=150)
        else:
            return "ok"
            


    def check_date(self):
        nowdate = dt.strftime(dt.now(), "%Y.%m.%d")
        try:
            return self.cursor.execute("ALTER TABLE Tabel ADD COLUMN '%s' 'TEXT'" % nowdate)
        except OperationalError:
            return "already exists"
        
        
    def read(self, user_id, column):
        with self.connection:
            #if 'column' in kwargs:
            try:
                return self.cursor.execute("select " + column + " from Tabel where id =?",(user_id,)).fetchone()
            #else:
            except OperationalError:
                return self.cursor.execute("select " + '"' + column + '"' + " from Tabel where id =?",(user_id,)).fetchone()
                #return "Err"
      
      
    def upd(self,user_id,**kwargs):
        dictio = {}
        corr_dict={}
        self.check_date()
        tableinf = self.get_columns()
        
        for i in range(len(tableinf)):
            dictio.update({tableinf[i][1]:""})
        try:
            for key in kwargs:
                if key in dictio:
                    dictio[key]=kwargs[key]                
                elif key == "timeOn":
                    nowdate = dt.strftime(dt.now(), "%Y.%m.%d")
                    nowtime = dt.strftime(dt.now(), "%H:%M")
                    prev_time = self.read(user_id, '"' + nowdate + '"')[0]
                    if prev_time == None:
                        corr_dict.update({'"' + nowdate + '"':nowtime})
                    elif len(prev_time)>0 and prev_time != "empty":
                        corr_dict.update({'"' + nowdate + '"':prev_time + "-" +nowtime})
                    else:    
                        corr_dict.update({'"' + nowdate + '"':nowtime})
            for key in dictio:
                if dictio[key]=='':
                    #dictio.pop(key)
                    pass
                #elif '-' in key:
                #    corr_dict['"' + key + '"'] = dictio[key]  - были проблемы с форматом дат с тире, сделал их  с точкой

                else:
                    corr_dict[key]=dictio[key]
            
            #nocol = list(filter(lambda x:x not in dictio.keys(),kwargs.keys())) 
            #if len(nocol)>0:
            #    print( "no such column: {}".format(", ". join(nocol)))
            colstr = ', '.join("{!s}={!r}".format(key,val) for (key,val) in corr_dict.items())
            #print (" colstr= " + colstr)
            self.cursor.execute("update Tabel set " + colstr + " where id = ?",(user_id,))
            #print(" success")
            self.connection.commit()
            return "Вы были успешно добавлены"
        except ZeroDivisionError:
            return "Возникла непредвиденная ошибка при добавлении в базу (Ошибка 3)"
    
    
    def add(self,user_id, **kwargs):
         #print( "insert into Tabel values (" + ", ".join(["?" for i in get_columns()])+"),(user_id,"+",".join([str(value) for key,value in kwargs.items()])+","*(len(get_columns())-len(kwargs.items())-1)+")")
         arg_list = [user_id]
         for i in range(len(self.get_columns())-1):
             arg_list.append("empty")        
         self.connection.execute("insert into Tabel values (" + ", ".join(["?" for i in self.get_columns()])+")",(arg_list))  
         self.connection.commit()
         if len(kwargs)>0:
             right_kwargs=",".join("{}={}".format(key,value) for key,value in kwargs.items())
             return self.upd(user_id, **kwargs)
          
      
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()