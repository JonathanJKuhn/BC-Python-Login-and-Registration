from flask_app import app
from flask import render_template, redirect, request, session, flash
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
    
    pw_hash = bcrypt.generate_password_hash(request.form.get('password'))
    data['password'] = pw_hash
    new_user = User.add(data)
    session['id'] = new_user
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { 'email': request.form.get('email') }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form.get('password')):
        flash("Invalid Email/Password")
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    data = { 'id': session['id'] }
    user_data = User.get_user_by_id(data)
    return render_template('dashboard.html',title='Dashboard',user=user_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')