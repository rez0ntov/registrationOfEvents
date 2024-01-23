import math
import time
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

    def addMember(self,name,team):
        try:
            print(name)
            print(team)
            member=(name, team)
            self.query("""CREATE TABLE IF NOT EXISTS events(id INT AUTO_INCREMENT PRIMARY KEY, name text, team text)""")
            self.query("INSERT INTO member(name, team) VALUES(%s, %s)", member )
        except Exception as e:
            print(e)
            print("Ошибка добавления участника в БД ")
            return False
        return True

    def getMember(self, member_id):
        try:
            res=self.fetchone(f"SELECT * FROM member WHERE id = {member_id}")
            if not res:
                print("Участник не найден")
                return False
            return res
        except:
            print("Ошибка получения данных из БД ")

        return False