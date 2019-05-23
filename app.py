
from flask import Flask, render_template, request, redirect,url_for, flash
from db import Database
app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    return render_template('./auth/login.html')


@app.route('/home', methods=["POST"])
def home():
    db = Database()
    email = request.form.get('email')
    password = request.form.get('password')
    auth = db.login(email,password)
    if auth != None:
        return render_template('home.html')
    else:
        flash('Email or Password is wrong!!')
        return redirect(url_for('Index'))

@app.route('/register', methods=["POST", "GET"])
def register():
    db = Database()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        dbResponse = db.createUser(email,password)
        print(dbResponse)
        if dbResponse:
            flash('User Added Successfully')
            return redirect(url_for('Index'))
        else: 
            flash('User Added Fail')
            return redirect(url_for('Index'))
    elif request.method == 'GET':
        return render_template('./auth/register.html')
        

@app.route('/styles.css')
def sendStyles():
    return app.send_static_file('./templates/styles.css')
    

if __name__ == '__main__':
    app.run(debug=True)

