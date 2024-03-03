from flask_login import current_user, login_user, logout_user, login_manager, LoginManager, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from dbmodel import DBmanager
from UserLogin import UserLogin
from config import *
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
LoginManager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"
@login_manager.user_loader
def load_user(user_id):
    dbase = DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

@app.route("/", methods=["POST","GET"])
def login():
    dbase=DBmanager(host="mysql94.1gb.ru", user="gb_regkv", passwd="KHKFrmM-85pK", name="gb_regkv")
    if current_user.is_authenticated:
        return redirect(url_for('newstat'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user[3], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect( url_for("login"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html")


@app.route('/admin-password')
def reg():
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

@app.route("/admin_login")
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

