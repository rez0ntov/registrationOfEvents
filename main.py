from db import DatabaseManager
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

app.route("/registration")
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/read_form", methods=['POST'])
def read_form():
    users = DatabaseManager('users.db')
    users.create_tables()
    data=request.form
    userEmail = data['userEmail']
    userNmae = data['name']
    userLastname = data['lastname']
    dictsend = (userEmail, userNmae, userLastname)
    users.query('''INSERT INTO Users VALUES (?,?,?)''',dictsend)
    return render_template('read_form.html')