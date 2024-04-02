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
    base = DBmanager(host, user, password, name)
    try:
        result = base.fetchall('''SELECT name, DATE_FORMAT(date1, '%d.%m'),    
                                  CASE
                                      WHEN date2 = date1 
                                          THEN ' ' 
                                      WHEN date2 <> date1 
                                          THEN DATE_FORMAT(date2, '%d.%m')
                                  END AS date2,
                                  CASE
                                      WHEN date2 <> date1
                                          THEN '-'
                                      WHEN date2 = date1 
                                          THEN '' 
                                  END AS cherta
                                  FROM EEvents
                                  WHERE CURRENT_DATE() >= date1 and CURRENT_DATE() <= date2''')
        for x in result:
            print(x)
    except:
        print('error')
    return render_template('index.html', result=result)


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
        result = base.fetchall('''SELECT name, DATE_FORMAT(date1, '%d.%m'),    
                                  CASE
                                      WHEN date2 = date1 
                                          THEN ' ' 
                                      WHEN date2 <> date1 
                                          THEN DATE_FORMAT(date2, '%d.%m')
                                  END AS date2,
                                  CASE
                                      WHEN CURRENT_DATE() >= date1 and CURRENT_DATE() <= date2
                                          THEN 'сегодня' 
                                      WHEN CURRENT_DATE() < date1 or CURRENT_DATE() > date2
                                          THEN ' '
                                  END AS active,
                                  CASE
                                      WHEN date2 <> date1
                                          THEN '-'
                                      WHEN date2 = date1 
                                          THEN '' 
                                  END AS cherta
                                  FROM еEvents;''')
        for x in result:
            print(x)
    except:
        print('error')
    return render_template('eventslist.html',result=result)

# @app.route("/eventslist")
# def eventslist():
#     base = DBmanager(host, user, password, name)
#     try:
#         result = base.fetchall('''SELECT name from eEvents''')
#         for x in result:
#             print(x)
#     except:
#         print('error')
#     return render_template('eventslist.html',result=result)


# @app.route("/read_form", methods=['POST'])
# def read_form():
#     base = DBmanager(host,user,password,name)
#     base.query('''CREATE TABLE IF NOT EXISTS Events(name text, date date, team text)''')
#     data = request.form
#     eventname = data['eventName']
#     date = data['date']
#     team = data['team']
#     dictsend = (eventname, date, team)
#     base.query('''INSERT INTO Events(name, date, team) VALUES (%s, %s, %s)''', dictsend)
#     return render_template('read_form.html')

# @app.route("/read_createevent", methods=['POST'])
# def read_createevent():
#     base = DBmanager(host,user,password,name)
#     result = base.query('''SELECT * FROM eevents WHERE name = eventname''') 
    
#     if result:
#         return render_template('error.html')
#     else:
#         base.query('''CREATE TABLE IF NOT EXISTS eEvents(name text, date1 date, date2 date, team text)''')
#         data = request.form
#         eventName = data['eventName']
#         date1 = data['date1']
#         date2 = data['date2']
#         team = data['team']
#         dictsend = (eventName, date1, date2, team)
#         base.query('''INSERT INTO eEvents(name, date1, date2, team) VALUES (%s, %s, %s, %s) ''', dictsend)
#     return render_template('createevent.html')

@app.route("/read_createevent", methods=['POST'])
def read_createevent():
    base = DBmanager(host, user, password, name)
    data = request.form
    eventName = data['eventName']
    date1 = data['date1']
    date2 = data['date2']
    team = data['team']
    
    result = base.fetchone('''SELECT name FROM eEvents WHERE name = %s''', (eventName,))
    print(result)
    
    if result:
        return render_template('error.html')
    else:
        dictsend = (eventName, date1, date2, team)
        base.query('''INSERT INTO eEvents(name, date1, date2, team) VALUES (%s, %s, %s, %s) ''', dictsend)
        return render_template('createevent.html')



# @app.route("/read_createevent", methods=['POST'])
# def read_createevent():
#     base = DBmanager(host,user,password,name)
#     base.query('''CREATE TABLE IF NOT EXISTS eEvents(name, date1 date, date2 date, team text)''')
    
#     data = request.form
#     eventname = data['eventName']
#     date1 = data['date1']
#     date2 = data['date2']
#     team = data['team']

#     result = base.query('''SELECT * FROM eEvents WHERE name = %s''', (eventname,))
    
#     if result:
#         return render_template('error.html')
#     else:
#         dictsend = (eventname, date1, date2, team)
#         base.query('''INSERT INTO eEvents(name, date1, date2, team) VALUES (%s, %s, %s, %s) ''', dictsend)
#         return render_template('createevent.html')


@app.route("/error")
def error():
    return render_template('error.html')

# @app.route('/<id>')
# def show_page(id):
#     base = DBmanager(host,user,password,name)
#     result = base.query("SELECT * FROM EEvents WHERE id = %s", (id,))

#     if result:
#         return render_template('event_id.html', result=result)
#     else:
#         return "Page not found"


@app.route("/event<id>")
def event(id):
     base = DBmanager(host, user, password, name)
     try:
         result = base.fetchall(f"SELECT name, date1, date2, team, id FROM EEvents WHERE id = {id}")
         print(result)
     except:
        print('error')
     return render_template('event_id.html',result=result)

@app.route("/update_event", methods=['POST'])
def update_event():
    base = DBmanager(host,user,password,name)
    data = request.get_json()
    id = data['id']
    eventname = data['eventName']
    date1 = data['date1']
    date2 = data['date2']
    base.query("UPDATE EEvents SET name = %s, date1 = %s, date2 = %s, team = %s WHERE id = %s", (eventname, date1, date2, id))
    
    return render_template('event_id.html',result=result)





if __name__ == '__main__':
    app.run(debug=True)

