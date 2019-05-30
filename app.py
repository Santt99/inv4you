import os
from flask import Flask, render_template, request, redirect,url_for, flash, session
from db import Database
from werkzeug.utils import secure_filename
import pandas as pd
import sqlalchemy
import pymysql
app = Flask(__name__)
import json
# settings
app.secret_key = "mysecretkey"
UPLOAD_FOLDER = 'invs/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def Index():
    if 'id' in session: 
            inventories = db.searchForUserInventories(session['id'])
            flash('User Logged Successfully')
            return render_template('home.html', inventories=inventories)
    else:
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
        tableTitle = db.getTableNameById(id)
        res = db.deleteInventory(id,tableTitle[0]['title'])
        if res:
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
        res = db.extractTableData(tableTitle[0]["title"])
        columns = set()
        for key in res[0].keys():
            columns.add(key)
        flash('User Logged Successfully')
        return render_template('edit.html', columns=columns, title=tableTitle[0]["title"], id=id, data=res)
    else:
        redirect(url_for("Index"))


@app.route('/newRow/<id>', methods=["POST", "GET"])
def createNewRow(id):
    if 'id' in session:
        if request.method == 'POST':
            tableTitle = db.getTableNameById(id)
            res = db.extractTableData(tableTitle[0]["title"])
            columns = []
            for key in res[0].keys():
                if key != 'id':
                    columns.append(key)
            values = []
            for column in columns:
                values.append(request.form.get(column))
                
            res = db.addCustomRow(tableTitle[0]["title"],columns,values)
            flash('User Logged Successfully')
            return redirect(url_for('Home'))
        elif request.method == 'GET':
            tableTitle = db.getTableNameById(id)
            res = db.extractTableData(tableTitle[0]["title"])
            columns = set()
            for key in res[0].keys():
                if key != 'id':
                    columns.add(key)
            return render_template('./addRow.html', id=id, columns=columns)
    else:
        redirect(url_for("Index"))

@app.route('/addColumn/<id>', methods=["POST", "GET"])
def addColumnToTable(id):
    if 'id' in session:
        if request.method == 'POST':
            newColumnTitle = request.form.get('columnTitle')
            tableTitle = db.getTableNameById(id)
            print(tableTitle)
            response = db.addColumn(tableTitle[0]['title'],newColumnTitle)
            if response:
                flash('User Logged Successfully')
                return redirect(url_for('Home'))
            else:
                return "Error, the column can't be added!"
        elif request.method == 'GET':
            return render_template('./addColumn.html', id=id)
        
    else:
        redirect(url_for("Index")) 
@app.route('/search/<id>', methods=["POST", "GET"])
def search(id):
    if 'id' in session:
        tableTitle = db.getTableNameById(id)
        table = tableTitle[0]["title"]
        if request.method == 'POST':
            res = db.extractTableData(table)
            typeOfData = request.form.get('typeOfData')
            valueToSearch = request.form.get('search')
            res = db.searchForDataInTableByColumn(table, typeOfData, valueToSearch)
            columns = set()
            try:
                for key in res[0].keys():
                    if key != 'id':
                        columns.add(key)
                flash('User Logged Successfully')
                return render_template('edit.html', columns=columns, title=valueToSearch, id=id, data=res)
            except:
                return "Nothing like " + valueToSearch + " found in " + typeOfData + "." 
        elif request.method == 'GET':
            tableTitle = db.getTableNameById(id)
            res = db.extractTableData(table)
            columns = set()
            for key in res[0].keys():
                if key != 'id':
                    columns.add(key)
            print(columns)
            return render_template('./searchByColumn.html', id=id, columns=columns)
    else:
        redirect(url_for("Index"))


@app.route('/editRow/<tableId>/<rowId>', methods=["POST", "GET"])
def editRow(tableId, rowId):
    if 'id' in session:
        if request.method == 'POST':
            tableTitle = db.getTableNameById(tableId)
            res = db.extractTableData(tableTitle[0]["title"])
            columns = []
            for key in res[0].keys():
                if key != 'id':
                    columns.append(key)
            values = []
            for column in columns:
                values.append(request.form.get(column))
                
            res = db.editCustomRow(tableTitle[0]["title"],rowId,columns,values)
            return "Done!"
        elif request.method == 'GET':
            tableTitle = db.getTableNameById(tableId)
            res = db.extractTableData(tableTitle[0]["title"])
            data = db.searchForRowDataById(rowId, tableTitle[0]["title"])
            return render_template('./editRow.html', tableId=tableId, rowId=rowId, columns=data)
    else:
        redirect(url_for("Index"))

@app.route('/saveNewInv', methods=["POST"])
def saveNewInventory():
    if 'id' in session:
        title = request.form.get('title')
        des = request.form.get('description')
        sqlTCrea = db.createSQLTable(title)
        if sqlTCrea:
            response = db.createInventory(session['id'],title,des)
            if response:
                flash('User Logged Successfully')
                return redirect(url_for('Home'))
            else:
                return "Fail"
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
                    df = pd.read_csv(os.path.join(app.root_path,app.config["UPLOAD_FOLDER"],file.filename))
                    engine = sqlalchemy.create_engine('mysql://m7479tvdnwwfimqo:jse16k4dx7nd6l8l@a07yd3a6okcidwap.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/xpba22f95w8rrd8q')
                    print(df.to_sql(name=file.filename, con=engine, index=True, if_exists='replace', index_label='id'))
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
    app.run(debug=True, host='0.0.0.0')

