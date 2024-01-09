import math
import  time
from mysql.connector import connect, Error
class DBmanager:
    def __init__(self,host, user, passwd, name):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.name=name

    def query(self, arg, values=None):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.passwd,
                    database=self.name,
                    ssl_disabled=True,
            ) as connection:
                with connection.cursor() as cursor:
                    if values==None:
                        cursor.execute(arg)
                    else:
                        cursor.execute(arg, values)
                    connection.commit()
                    cursor.close()
                    connection.close()
        except Error as e:
            print(e)

    def fetchone(self, arg, values=None):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.passwd,
                    database=self.name,
                    ssl_disabled=True,
            ) as connection:
                with connection.cursor() as cursor:
                    if values==None:
                        cursor.execute(arg)
                    else:
                        cursor.execute(arg, values)
                    return cursor.fetchone()
        except Error as e:
            print(e)
            return None


    def fetchall(self, arg, values=None):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.passwd,
                    database=self.name,
                    ssl_disabled=True,
            ) as connection:
                with connection.cursor() as cursor:
                    if values==None:
                        cursor.execute(arg)
                    else:
                        cursor.execute(arg, values)
                    return cursor.fetchall()
        except Error as e:
            print(e)
            return None

    def addEvent(self,name, date, time, description ):
        try:
            print(name)
            print(date)
            print(time)
            print(description)
            event=(name, date, time, description)
            self.query("""CREATE TABLE IF NOT EXISTS events(id INT AUTO_INCREMENT PRIMARY KEY, name text, date text, time text, description text)""")
            self.query("INSERT INTO events(name, date, time, description) VALUES(%s, %s, %s)", event )
        except Exception as e:
            print(e)
            print("Ошибка добавления мероприятия в БД ")
            return False
        return True

    def getEvent(self, event_id):
        try:
            res=self.fetchone(f"SELECT * FROM events WHERE id = {event_id}")
            if not res:
                print("Мероприятие не найдено")
                return False
            return res
        except:
            print("Ошибка получения данных из БД ")

        return False