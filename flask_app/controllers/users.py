from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html',title='Home - Login & Reg')

@app.route('/register', methods=['POST'])
def register():
    data = {
        'fname': request.form.get('fname').capitalize(),
        'lname': request.form.get('lname').capitalize(),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'confirm': request.form.get('confirm'),
        'dob': request.form.get('dob')
    }
    # We want to keep the information that the user has input, so they can more easily correct inputs
    if not User.validate_registration(data):
        for key in data:
            session[key] = data[key]
        return redirect('/')
    
    session.clear()
    pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
    data['password'] = pw_hash
    new_user = {
        'id': User.add(data)
    }
    user_obj = User.get_user(new_user)
    for attr, value in user_obj.__dict__.items():
        session[attr] = value
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',title='Dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')