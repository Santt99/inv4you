
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./auth/login.html')

@app.route('/home', methods=["POST"])
def home():
    email = request.form.get('email')
    password = request.form.get('password')
    print(password)
    return 'home'

@app.route('/register')
def register():
    return render_template('./auth/register.html')
    

if __name__ == '__main__':
    app.run(debug=True)

