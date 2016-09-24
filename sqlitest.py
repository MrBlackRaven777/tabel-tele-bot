import sqlite3
import datetime
import random

def read_table(uid, column): 
# считывает значение из uid строки column столбца
 s=c.execute("select " +column + " from test where id=?", (uid,)).fetchone()
 return str(s[0])

def testdef(**kwargs):
 print(kwargs['column'])
 
def get_columns():
 try:
  return c.execute("pragma table_info(test)").fetchall()
 except:
  return false

def modify_db(user_id, mod_type = "read", **kwargs):
        """ Получаем одну строку с нужным нам id """
        #with self.connection:
        if mod_type == "read":
         if 'column' in kwargs:
          return c.execute("select " + kwargs['column'] + " from test where id =?",(user_id,)).fetchone()
         else:
          return false
       #не забыть ввести проверку на наличие колонки, мб отдельной функцией
        elif mod_type == "upd":
         dictio = {}
         corr_dict={}
         tableinf = c.execute("pragma table_info(test)").fetchall()
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
          c.execute("update test set " + colstr + " where id = ?",(user_id,))
          print(" success")
          conn.commit()
          return("ok")
         except ZeroDivisionError:
          print("err")
        elif mod_type=="add":
         #print( "insert into test values (" + ", ".join(["?" for i in get_columns()])+"),(user_id,"+",".join([str(value) for key,value in kwargs.items()])+","*(len(get_columns())-len(kwargs.items())-1)+")")
         arg_list = [user_id]
         for i in range(len(get_columns())-1):
          arg_list.append("empty")
         c.execute("insert into test values (" + ", ".join(["?" for i in get_columns()])+")",(arg_list))  
         conn.commit()
         right_kwargs=",".join("{}={}".format(key,value) for key,value in kwargs.items())
         #	print( ["no" for i in range(len(get_columns())-1)])
         print (right_kwargs)
         return modify_db(user_id, "upd", **kwargs)
          #self.cursor.execute("insert into Tabel
          	
#def insert(uid, column, value):
#вставить новую строку в базу, для нового uid

#def update(uid, column, value):
#обновить инфу существующего uid

conn = sqlite3.connect('/storage/sdcard0/org.qpython.qpy/myscripts/mydbtest.db')
c = conn.cursor()
#c.execute('''CREATE TABLE tabel (time1, time2, total)''')
nowdate = datetime.datetime.date(datetime.datetime.today())
print (nowdate)
data = c.execute("PRAGMA table_info(test)").fetchall()
cols = []
uid=random.random()*100
for i in range(len(data)):
 cols.append(data[i][1])
print(cols)
if str(nowdate) in cols:
 print('yes')
else:
 print('no')
 c.execute("ALTER TABLE test ADD COLUMN '%s' 'TEXT'" % nowdate)

#print(read_table(2, "read", column='value'))

#testdef(column='value')

#print(modify_db(2, "read", column='value'))
 
#print(modify_db(2,"upd",value=1468))#,mycol=str(nowdate),newcol='er',tewt=234))
data = str(nowdate)
print(modify_db(uid, "add", value=uid*2, mycol="text", data="14.30"))

#print ("insert into test values (" + ", ".join(["?" for i in get_columns()])+")")
#def insert(uid, column):
# dic = {"id" : '',"stavka":'',"value":'')

