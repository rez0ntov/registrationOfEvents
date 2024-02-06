from db import DBmanager
from config import *
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('form.html')
@app.route("/test")
def test():
    return render_template('reg.html')
@app.route("/registration")
def registration():
    return render_template('form.html')

@app.route("/read_form", methods=['POST'])
def read_form():
    base = DBmanager(host,user,password,name)
    self.qery('''CREATE TABLE IF NOT EXISTS Events(name text, date date, time text, members text)''')
    data=request.form
    event = text['event']
    date = data['date']
    team = text['team']
    members = text['members']
    dictsend = (event, date, team, members)
    users.query('''INSERT INTO Events VALUES (?,?,?,?)''',dictsend)
    return render_template('read_form.html')

if __name__ == '__main__':
    app.run(debug=True)

