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
    base = DBmanager(host, user, password, name)
    try:
        result = base.fetchall('SELECT * FROM Events')
        for x in result:
            print(x)
    except:
        print('error')
    return render_template('eventslist.html',result=result)

@app.route("/read_form", methods=['POST'])
def read_form():
    base = DBmanager(host,user,password,name)
    base.query('''CREATE TABLE IF NOT EXISTS Events(name text, date date, team text)''')
    data = request.form
    eventname = data['eventName']
    date = data['date']
    team = data['team']
    dictsend = (eventname, date, team)
    base.query('''INSERT INTO Events(name, date, team) VALUES (%s, %s, %s)''', dictsend)
    return render_template('read_form.html')

if __name__ == '__main__':
    app.run(debug=True)

