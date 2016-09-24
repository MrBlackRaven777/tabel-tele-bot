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
                return "Err"
      
      
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
            for key in dictio:
                if dictio[key]=='':
                    #dictio.pop(key)
                    pass
                #elif '-' in key:
                #    corr_dict['"' + key + '"'] = dictio[key]  - были проблемы с форматом дат с тире, сделал их  с точкой
                elif key == "timeOn":
                    nowdate = dt.strftime(dt.now(), "%Y.%m.%d")
                    nowtime = dt.strftime(dt.now(), "%H:%M")
                    corr_dict.update({nowdate:nowtime})
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
            return("Вы были успешно добавлены")
        except ZeroDivisionError:
            return("Возникла непредвиденная ошибка при добавлении в базу (Ошибка 3)")
    
    
    def add(self,user_id, **kwargs):
         #print( "insert into Tabel values (" + ", ".join(["?" for i in get_columns()])+"),(user_id,"+",".join([str(value) for key,value in kwargs.items()])+","*(len(get_columns())-len(kwargs.items())-1)+")")
         arg_list = [user_id]
         for i in range(len(self.get_columns())-1):
             arg_list.append("empty")
         self.connection.execute("insert into Tabel values (" + ", ".join(["?" for i in self.get_columns()])+")",(arg_list))  
         self.connection.commit()
         right_kwargs=",".join("{}={}".format(key,value) for key,value in kwargs.items())
         return self.upd(user_id, **kwargs)
          
      
      
            
    def modify_db(user_id, mod_type = "read", **kwargs):
        """ Получаем одну строку с нужным нам id """
        #with self.connection:
        if mod_type == "read":
         if 'column' in kwargs:
          return c.execute("select " + kwargs['column'] + " from Tabel where id =?",(user_id,)).fetchone()
         else:
          return false
       #не забыть ввести проверку на наличие колонки, мб отдельной функцией
        elif mod_type == "upd":
         dictio = {}
         corr_dict={}
         tableinf = c.execute("pragma table_info(Tabel)").fetchall()
         for i in range(len(tableinf)):
          dictio.update({tableinf[i][1]:""})
         try:
          for key in kwargs:
           if key in dictio:
            dictio[key]=kwargs[key]
          for key in dictio:
           if dictio[key]=='':
            #dictio.pop(key)
            print(key + " empt")
           elif '-' in key:
            corr_dict['"' + key + '"'] = dictio[key]            
           else:
            corr_dict[key]=dictio[key]
            
          nocol = list(filter(lambda x:x not in dictio.keys(),kwargs.keys())) 
          if len(nocol)>0:
           print( "no such column: {}".format(", ". join(nocol)))
          colstr = ', '.join("{!s}={!r}".format(key,val) for (key,val) in corr_dict.items())
          print (" colstr= " + colstr)
          c.execute("update Tabel set " + colstr + " where id = ?",(user_id,))
          print(" success")
          conn.commit()
          return("ok")
         except ZeroDivisionError:
          print("err")
        elif mod_type=="add":
         #print( "insert into Tabel values (" + ", ".join(["?" for i in get_columns()])+"),(user_id,"+",".join([str(value) for key,value in kwargs.items()])+","*(len(get_columns())-len(kwargs.items())-1)+")")
         arg_list = [user_id]
         for i in range(len(get_columns())-1):
          arg_list.append("empty")
         c.execute("insert into Tabel values (" + ", ".join(["?" for i in get_columns()])+")",(arg_list))  
         conn.commit()
         right_kwargs=",".join("{}={}".format(key,value) for key,value in kwargs.items())
         #    print( ["no" for i in range(len(get_columns())-1)])
         print (right_kwargs)
         return modify_db(user_id, "upd", **kwargs)
          #self.cursor.execute("insert into Tabel

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()