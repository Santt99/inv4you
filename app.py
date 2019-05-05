
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./auth/login.html', stat="")

@app.route('/home', methods=["POST"])
def home():
    email = request.form.get('email')
    password = request.form.get('password')
    print(len(email))
    print(len(password))
    return 'home'

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        emailLength = len(email)
        passwordLength = len(password)
        if  emailLength > 0 and emailLength < 51 and passwordLength > 0 and passwordLength < 51:
            print(email)
            prin
            return render_template('./auth/login.html', stat = "User Register Succed!")
    elif request.method == 'GET':
        return render_template('./auth/register.html')
        

@app.route('/styles.css')
def sendStyles():
    return app.send_static_file('./templates/styles.css')
    

if __name__ == '__main__':
    app.run(debug=True)

