from dbCreateEvents import DBmanager
from config import *
base = DBmanager(host,user,password,name)
base.query("""CREATE TABLE IF NOT EXISTS events(id INT AUTO_INCREMENT PRIMARY KEY, name text, date text, time text, description text)""")
# base.addEvent('ВСЕРОС', "20.08.2024" , '18:00','Проведение Всероссийской олимпиады школьников по работотехники'fhgfhfh)