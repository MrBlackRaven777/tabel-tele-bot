import sqlite3

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

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()