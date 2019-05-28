import os
from flask import Flask, render_template, request, redirect,url_for, flash, session
from db import Database
from werkzeug.utils import secure_filename
import pandas as pd
import sqlalchemy
app = Flask(__name__)
import json

# settings
app.secret_key = "mysecretkey"
UPLOAD_FOLDER = '/home/s3xy/Documents/university/plugins/inv4you/invs/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def Index():
    return render_template('./auth/login.html')

db = Database()

@app.route('/home', methods=["POST", "GET"])
def Home():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        auth = db.login(email,password)
        if auth != None :
            session['id'] = auth['users_id']
            inventories = db.searchForUserInventories(auth['users_id'])
            flash('User Logged Successfully')
            return render_template('home.html', inventories=inventories)
        else:
            flash('Email or Password is wrong!!')
            return redirect(url_for('Index'))
    elif request.method == "GET":
        if 'id' in session: 
            inventories = db.searchForUserInventories(session['id'])
            flash('User Logged Successfully')
            return render_template('home.html', inventories=inventories)
        else:
            redirect(url_for(Index))


@app.route('/delete/<id>')
def delete(id):
    if 'id' in session:
        res = db.deleteInventory(id)
        if(res):
            flash('User Logged Successfully')
            return redirect(url_for('Home'))
    else:
        redirect(url_for(Index))

@app.route('/create')
def create():
    if 'id' in session: 
        flash('User Logged Successfully')
        return render_template('createNewInv.html')
    else:
        redirect(url_for(Index))

@app.route('/edit/<id>')
def edit(id):
    if 'id' in session: 
        tableTitle = db.getTableNameById(id)
        print(tableTitle[0]["title"])
        res = db.extractTableData(tableTitle[0]["title"])
        columns = set()
        for key in res[0].keys():
            columns.add(key)
        flash('User Logged Successfully')
        return render_template('edit.html', columns= columns, title=tableTitle[0]["title"], id=id, data=res).encode('unicode')
    else:
        redirect(url_for(Index))


@app.route('/saveNewInv', methods=["POST"])
def saveNewInventory():
    if 'id' in session:
        title = request.form.get('title')
        des = request.form.get('description')
        response = db.createInventory(session['id'],title,des)
        if response:
            flash('User Logged Successfully')
            return redirect(url_for('Home'))
        else:
            return "Fail"
    else:
        redirect(url_for(Index))   

@app.route('/register', methods=["POST", "GET"])
def register():
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


@app.route('/uploadInv', methods=["POST", "GET"])
def uploadInv():
    if 'id' in session:
        if request.method == 'POST':
                if request.files :
                    file = request.files["inv"]
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"],file.filename))
                    df = pd.read_csv(os.path.join(app.config["UPLOAD_FOLDER"],file.filename))
                    engine = sqlalchemy.create_engine('mysql://m7479tvdnwwfimqo:jse16k4dx7nd6l8l@a07yd3a6okcidwap.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/xpba22f95w8rrd8q')
                    print(df.to_sql(name=file.filename, con=engine, index=False, if_exists='replace'))
                    print(file.filename + " saved!")
                    des = request.form.get('description')
                    response = db.createInventory(session['id'], file.filename, des)
                    if response:
                        flash('User Logged Successfully')
                        return redirect(url_for('Home'))
                    else:
                        return "Fail"
        elif request.method == 'GET':        
            flash('User Logged Successfully')
            return render_template('uploadInventory.html')
    else:
        redirect(url_for(Index))

@app.route('/styles.css')
def sendStyles():
    return app.send_static_file('./templates/styles.css')
    

if __name__ == '__main__':
    app.run(debug=True)

