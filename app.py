
from flask import Flask, render_template, request, redirect,url_for
from db import Database
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./auth/login.html')


@app.route('/home', methods=["POST"])
def home():
    db = Database()
    email = request.form.get('email')
    password = request.form.get('password')
    auth = db.login(email,password)
    if auth != None:
        return 'home'
    else:
        return redirect('/')

@app.route('/register', methods=["POST", "GET"])
def register():
    db = Database()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        dbResponse = db.createUser(email,password)
        if dbResponse:
            return redirect('/')
        else: 
            return redirect('/')
    elif request.method == 'GET':
        return render_template('./auth/register.html')
        

@app.route('/styles.css')
def sendStyles():
    return app.send_static_file('./templates/styles.css')
    

if __name__ == '__main__':
    app.run(debug=True)

