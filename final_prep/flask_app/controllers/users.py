from flask_app import app
from flask import render_template, flash, session, redirect, request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt= Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')
# Returns to index.html

@app.route('/users/register', methods=['POST'])
def register_user():
    data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password':request.form['password'],
        'confirm_password':request.form['confirm_password']
        }
    if User.validate_new_user(data):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_user_data = {
            'first_name': request.form['first_name'],
            'last_name':request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        User.create_new_user(new_user_data)
        flash('User created; login now')
        return redirect('/')
        
    else:
        print('User does not pass validation')
        return redirect('/')
# Register new user and hash password

@app.route('/users/login', methods=['POST'])
def login_user():
    user=User.get_user_by_email(request.form)
    if user==None:
        flash("No user found with that email")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password")
        return redirect('/')

    print('User passes validation')
    session['user_id']=user.id
    session['user_first_name']=user.first_name
    session['user_last_name']=user.last_name
    session['user_email']=user.email
    return redirect('/dashboard')
# Login user and send to dashboard

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash("This page is only available to logged in users")
        return redirect('/')
    return render_template('success.html')
# Successful login

@app.route('/users/logout')
def logout():
    session.clear()
    flash("You have logged out")
    return redirect('/')
# Log out user and send to index.html