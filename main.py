from dbmodel import DBmanager
from config import *
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def admin_login():
    return admin_login('admin_login.html')
@app.route("/form.html")
def form():
    return form('form.html')

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

