from flask_app import app
from flask import Flask, render_template, session, redirect, request
from flask_app.models.user import User

# Accesses /create in url to open create.html
@app.route('/create')
def index():

    return render_template('create.html')

#  Prepares user info for creation using request.form 
#  And carries it over to the /create/user 
@app.post('/create/user') 
def new_user():
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
# Function used to insert user into database, 
# passing data thru. No html goes here.
    User.create_new_user(data)
    return redirect('/show')

@app.route('/')
def home():
    return render_template('index.html')

# Access /show in url to open show.html
@app.route('/show')
def show():
    all_users=User.get_all()
    return render_template('show.html', all_users=all_users)

@app.route('/edit/<int:id>')
def edit(id):
    data={
        'id':id
    }
    one_user=User.get_one(data)
    return render_template('edit.html', one_user=one_user)

@app.post('/update/user/<int:id>')
def update_user(id):
    data={
    'first_name':request.form['first_name'],
    'last_name':request.form['last_name'],
    'email':request.form['email'],
    'id':id
    }
    User.update_user(data)
    return redirect('/show')

@app.route('/delete/<int:id>')
def delete_user(id):
    data={
        'id':id
    }
    User.destroy_user(data)
    return redirect('/show')