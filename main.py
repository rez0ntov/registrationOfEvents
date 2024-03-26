from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from dbmodel import DBmanager
from UserLogin import UserLogin
from config import *
from flask import Flask, render_template, request, redirect, url_for, flash
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"
app.secret_key = SECRET_KEY


# !!! email: adminemail11@gmail.com password: adminpasswd !!! #

@login_manager.user_loader
def load_user(user_id):
    dbase = DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
    print("load_user")
    return UserLogin().fromDB(int(user_id), dbase)


# @app.route("/login", methods=["POST","GET"])
# def login():
#     dbase = DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#
#     if request.method == "POST":
#         user = dbase.getUserByEmail(request.form['email'])
#         if user and check_password_hash(user[3], request.form['psw']):
#             userlogin = UserLogin().create(user)
#             rm = True if request.form.get('remainme') else False
#             login_user(userlogin, remember=rm)
#             return redirect( url_for("login"))
#
#         flash("Неверная пара логин/пароль", "error")
#
#     return render_template("login.html")


@app.route('/log')
def log():
    return render_template('login.html')


@app.route("/register", methods=["POST","GET"])
def register():
    dbase = DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
    print(request.form['psw'])
    hash = generate_password_hash(request.form['psw'])
    res = dbase.addUser(request.form['name'], request.form['email'], hash)
    print(res)
    return render_template("register.html")


@app.route('/reg')
def reg():
    return render_template('reg.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route("/")
@app.route("/login", methods=["POST","GET"])
def login():
    dbase = DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user[3], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect( url_for("login"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html")
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/createevent")
def createevent():
    return render_template('createevent.html')



@app.route("/eventslist")
def eventslist():
    base = DBmanager(host, user, password, name)
    try:
        result = base.fetchall('''SELECT name, DATE_FORMAT(date1, '%d.%m'), DATE_FORMAT(time1, '%H.%i'), DATE_FORMAT(date2, '%d.%m'), DATE_FORMAT(time2, '%H.%i') FROM events''')
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

@app.route("/read_createevent", methods=['POST'])
def read_createevent():
    base = DBmanager(host,user,password,name)
    base.query('''CREATE TABLE IF NOT EXISTS events(name text, date1 date, time1 time, date2 date, time2 time, team bool)''')
    data = request.form
    eventname = data['eventName']
    date1 = data['date1']
    time1 = data['time1']
    date2 = data['date2']
    time2 = data['time2']
    team = data['team']
    dictsend = (eventname, date1, time1, date2, time2, team)
    base.query('''INSERT INTO events(name, date1, time1, date2, time2, team) VALUES (%s, %s, %s, %s, %s, %s)''', dictsend)
    return render_template('createevent.html')


if __name__ == '__main__':
    app.run(debug=True)

