import psycopg2
from psycopg2 import ProgrammingError
from datetime import datetime as dt
from psycopg2.psycopg1 import cursor
#from config_bot import database_name as database

#Этот класс для работы с psycopg2
class PostGreSQL:
    
    def __init__(self):
        self.connection = psycopg2.connect("dbname=tabel user=postgres password=4589163")
        self.cursor = self.connection.cursor()

    def select_single(self, user_id):
        """ Получаем одну строку с нужным нам id """
        with self.connection:
            tr = self.cursor.execute('SELECT * FROM Tabel WHERE id = ?', (user_id,))
            if tr == []:
                self.cursor.execute('INSERT INTO Tabel VALUES (?,?,?,?)', (user_id,"150","false",""))
                self.connection.commit()
                return "You have been added"
            else:
                return "Your id is {}".format(tr[0])
            
    def get_columns(self):
        #try:
            #column_names = []
            #self.cursor.execute("""select column_name from information_schema.columns where table_name='tabel'""")
            #column_names = [row[0] for row in self.cursor]
            #return column_names
            self.cursor.execute("Select * FROM Tabel")
            colnames = [desc[0] for desc in self.cursor.description]
            return colnames
        #except:
            #return "false"

    def check_user(self,user_id):
        try:
            usr = self.cursor.execute('SELECT * FROM Tabel WHERE id=?',(user_id,))
        except ProgrammingError:
            self.add(user_id,stavka=150)

            

    def check_date(self):
        nowdate = dt.date(dt.now())
        try:
            self.cursor.execute('ALTER TABLE Tabel ADD COLUMN "%s" TEXT' % nowdate)
            self.connection.commit()
        except ProgrammingError:
            return "already exists"
        
        
    def read(self, user_id, column):
        with self.connection:
            #if 'column' in kwargs:
            try:
                return self.cursor.execute("select " + column + " from Tabel where id =?",(user_id,))
            #else:
            except OperationalError:
                return self.cursor.execute("select " + '"' + column + '"' + " from Tabel where id =?",(user_id,))
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