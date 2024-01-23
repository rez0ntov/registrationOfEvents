from dbCreateEvents import DBmanager
from config import *
base = DBmanager(host,user,password,name)
base.query("""CREATE TABLE IF NOT EXISTS events(id INT AUTO_INCREMENT PRIMARY KEY, name text, date text, time text)""")
# base.addEvent('ВСЕРОС1', "20.08.2025" , '19:00','Проведение Всероссийской олимпиады школьников по информатике'fhgfhfh)