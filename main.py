from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from dbmodel import DBmanager
from UserLogin import UserLogin
from config import *
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import qrcode
from io import BytesIO

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


@app.route("/register", methods=["POST", "GET"])
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
def aut():
    print('aut')
    return render_template("login.html")


@app.route("/login", methods=["POST"])
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
            return redirect(url_for("index"))

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
                                  END AS cherta,
                                  id
                                  FROM EEvents
                                  WHERE CURRENT_DATE() >= date1 and CURRENT_DATE() <= date2
                                  order by date1 desc;''')
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


@app.route("/pages-register")
def pages_register():
    return render_template('register.html')


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
                                  END AS cherta,
                                  id
                                  FROM EEvents
                                  order by date1 desc;
                                  ''')
        for x in result:
            print(x)

        data = request.form
        id = data['id']
        base.query('''DELETE FROM EEvents WHERE id = %s''', (id,))

    except:
        print('error')
    return render_template('eventslist.html', result=result)


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

    result = base.fetchone('''SELECT name FROM EEvents WHERE name = %s''', (eventName,))
    print(result)

    if result:
        return render_template('error.html')
    else:
        dictsend = (eventName, date1, date2, team)
        base.query('''INSERT INTO EEvents(name, date1, date2, team) VALUES (%s, %s, %s, %s) ''', dictsend)
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


# @app.route("/event<eventName>")
# def event(eventName):
#      base = DBmanager(host, user, password, name)
#      try:
#          result = base.fetchone('''SELECT team FROM eEvents WHERE name = %s''', (eventName))
#          print(result)
#      except:
#         print('error')
#      return render_template('event_id.html',result=result)


@app.route("/event<id>")
def event(id):
    base = DBmanager(host, user, password, name)
    try:
        print(id)
        result = base.fetchall(f"SELECT name, date1, date2, team, id FROM EEvents WHERE id = {id}")
        print(result)
    except:
        print('error')
    return render_template('event_id.html', result=result, id=id)


@app.route("/eventregister<id>")
def eventregister(id):
    base = DBmanager(host, user, password, name)
    try:
        result = base.fetchall(f"SELECT name, id, team FROM EEvents WHERE id = {id}")
        print(result)

        if result and result[0][2] == 'Команды':
            return render_template('team.html', result=result)

        elif result and result[0][2] == 'Участники':
            return render_template('participants.html', result=result)
        else:
            return "Не удалось определить тип команды"

    except:
        print('error')
        return "Произошла ошибка"


@app.route("/table<id>")
def table(id):
    base = DBmanager(host, user, password, name)
    try:
        print(id)
        result = base.fetchall(f"SELECT name, id, team FROM EEvents WHERE id = {id}")
        print(result)

        if result and result[0][2] == 'Команды':
            result = base.fetchall(f"SELECT DISTINCT tname from table_{id}")
            return render_template('tablet.html', result=result, id=id)

        elif result and result[0][2] == 'Участники':
            result = base.fetchall(f"SELECT pname, name2, name3, email4 FROM table_{id}")
            for x in result:
                print(x)
            return render_template('tablep.html', result=result, id=id)

        else:
            return "Не удалось определить тип команды"

    except:
        print('error')
        return render_template('nikto.html')

@app.route("/monitoring/<id>")
def monitoring(id):
    base = DBmanager(host, user, password, name)
    try:
        print(id)
        result = base.fetchall(f"SELECT pname, name2, name3 FROM table_{id} WHERE active = True")
        for x in result:
            print(x)
        result_2 = base.fetchall(f"SELECT pname, name2, name3 FROM table_{id} WHERE active = False")
        for x in result_2:
            print(x)
        return render_template('monitoring.html', result=result, id=id, result_2=result_2)
    except Exception as e:
        print('error:', e)
        result = []  
    return render_template('activnet.html')

# @app.route("/change/<id>/<tname>/<pid>")
# def chage(id, tname):
#     base = DBmanager(host, user, password, name)
#     try:
#         result = base.fetchall(f"SELECT pname, name2, name3 FROM table_{id} WHERE id = {id}")
#         print(result)
#         return render_template('change.html', result=result)
#     except Exception as e:
#         print('error:', e)
#         result = []  
#     return render_template('activnet.html')

@app.route("/teamlist/<int:id>/<tname>")
def teamlist(id, tname):
    base = DBmanager(host, user, password, name)
    try:
        print(tname)
        print(id)
        result = base.fetchall("SELECT id, pname, name2, name3, email4 FROM table_%s WHERE tname = %s", (id, tname))
        print(f"Result: {result}")  


        if not result:
            return "No teams found with the specified name."
        
        for x in result:
            print(x)
        
        return render_template('teamlist.html', result=result, tname=tname, id=id)

    except Exception as e:
        print(f'Error: {e}')
        return "An error occurred while processing your request."

@app.route('/generate_qr/<page_id>')
def generate_qr(page_id):
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'https://127.0.0.1:5000/active{page_id}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    
    img_byte_array = BytesIO()
    img.save(img_byte_array)
    img_byte_array.seek(0)

  
    return send_file(img_byte_array, mimetype='image/png')


@app.route("/active<page_id>")
def active(page_id):
    print(page_id)
    return render_template('active.html', page_id=page_id)


@app.route("/read_active", methods=['POST'])
def read_active():
    base = DBmanager(host, user, password, name)
    data = request.form
    page_id = data['page_id']
    pname = data['pname']
    name2 = data['name2']
    name3 = data['name3']
    dictsend = (pname, name2, name3)
    base.query(f"UPDATE table_{page_id} SET active = True WHERE pname = %s AND name2 = %s AND name3 = %s", dictsend)
    return render_template('active.html')


@app.route("/read_participants", methods=['POST'])
def read_participants():
    base = DBmanager(host, user, password, name)
    data = request.form
    id = data['id']
    base.query(
        f'CREATE TABLE IF NOT EXISTS table_{id} (id int AUTO_INCREMENT PRIMARY KEY, pname text, name2 text, name3 text, email4 text, active boolean DEFAULT False)')
    pname = data['pname']
    name2 = data['name2']
    name3 = data['name3']
    email4 = data['email4']
    dictsend = (pname, name2, name3, email4)
    base.query(f"INSERT INTO table_{id} (pname, name2, name3, email4) VALUES (%s, %s, %s, %s)", dictsend)
    return render_template('read_participants.html')


@app.route("/read_team", methods=['POST'])
def read_team():
    base = DBmanager(host, user, password, name)
    data = request.form
    id = data['id']
    base.query(
        f'CREATE TABLE IF NOT EXISTS table_{id} (id int AUTO_INCREMENT PRIMARY KEY, tname text, pname text, name2 text, name3 text, email4 text)')
    tname = data['tname']
    pname = data['pname']
    name2 = data['name2']
    name3 = data['name3']
    email4 = data['email4']
    dictsend = (tname, pname, name2, name3, email4)
    base.query(f"INSERT INTO table_{id} (tname, pname, name2, name3, email4) VALUES (%s, %s, %s, %s, %s)", dictsend)
    return render_template('read_participants.html')


@app.route("/update_event", methods=['POST'])
def update_event():
    base = DBmanager(host, user, password, name)
    data = request.form
    id = data['id']
    eventname = data['eventName']
    date1 = data['date1']
    date2 = data['date2']
    team = data['team']
    id = data['id']
    dictsend = (eventname, date1, date2, team, id)
    base.query('''UPDATE EEvents SET name = %s, date1 = %s, date2 = %s, team = %s WHERE id = %s''', dictsend)
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
                                      END AS cherta,
                                      id
                                      FROM EEvents
                                      order by date1 desc;
                                      ''')
        for x in result:
            print(x)


    except:
        print('error')

    return render_template('update_event.html', result=result)


@app.route("/delete_event", methods=['POST'])
def delete_event():
    base = DBmanager(host, user, password, name)
    data = request.form
    id = data['id']
    base.query('''DELETE FROM EEvents WHERE id = %s''', (id,))
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
                                      END AS cherta,
                                      id
                                      FROM EEvents
                                      order by date1 desc;
                                      ''')
        for x in result:
            print(x)


    except:
        print('error')

    return render_template('delete_event.html', result=result)


# @app.route("/update_event", methods=['POST'])
# def update_event():
#     base = DBmanager(host,user,password,name)
#     data = request.get_json()
#     id = data['id']
#     eventname = data['eventName']
#     date1 = data['date1']
#     date2 = data['date2']
#     base.query("UPDATE EEvents SET name = %s, date1 = %s, date2 = %s, team = %s WHERE id = %s", (eventname, date1, date2, id))

#     return render_template('event_id.html',result=result)


if __name__ == '__main__':
    app.run(debug=True)