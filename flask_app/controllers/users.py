from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html',title='Home - Login & Reg')

@app.route('/register', methods=['POST'])
def register():
    #validate

    pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
    data = {
        'password': pw_hash
    }