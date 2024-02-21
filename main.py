import mysql.connector
from dbmodel import DBmanager
from config import *
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/")
def admin_login():
    return render_template('admin_login.html')
@app.route("/form")
def form():
    return render_template('form.html')
@app.route("/eventslist")
def eventslist():
    myconn = mysql.connector.connect(host="mysql94.1gb.ru", user="gb_regkv", password="KHKFrmM-85pK", database="gb_regkv")
    cur=myconn.cursor()
    try:
        cur.execute('SELECT * FROM Events')
        result = cur.fetchall()
        for x in result:
            print(x)
    except:
        myconn.rollback()
    myconn.close()
    return render_template('eventslist.html',result=result)

@app.route("/read_form", methods=['POST'])
def read_form():
    base = DBmanager(host,user,password,name)
    base.query('''CREATE TABLE IF NOT EXISTS Events(name text, date date, team text, members text)''')
    data = request.form
    eventname = data['eventName']
    date = data['date']
    team = data['team']
    members = data['members']
    dictsend = (eventname, date, team, members)
    base.query('''INSERT INTO Events(name, date, team, members) VALUES (%s, %s, %s, %s)''', dictsend)
    return render_template('read_form.html')

if __name__ == '__main__':
    app.run(debug=True)

