from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def innerpage():
    return render_template('innerpage.html')

if __name__ == '__main__':
    app.run(debug=True)