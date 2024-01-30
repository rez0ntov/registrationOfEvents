from dbMember import DBmanager
from config import *
base = DBmanager(host,user,password,name)
base.query("""CREATE TABLE IF NOT EXISTS member(id INT AUTO_INCREMENT PRIMARY KEY, name text, team text)""")
base.addMember('sasha', 'school36')