from flask_app import app
from flask import render_template, flash, session, redirect, request
from flask_app.models.user import User
from flask_app.models.show import Show

@app.route('/dashboard')
def exam_dashboard():
    if 'user_id' not in session:
        flash("This page is only available to logged in users")
        return redirect('/')
    shows=Show.get_all_shows()
    return render_template('shows.html', shows=shows)
# Once logged in, takes user to dashboard

@app.route('/shows/new')
def new_show():
    return render_template('new_show.html')
# Returns to create show screen

@app.route('/shows/create', methods=['POST'])
def create_show():
    if Show.validate_show(request.form):
        data={
            'name':request.form['show_name'],
            'date':request.form['show_date'],
            'description':request.form['show_description'],
            'creator_id':session['user_id']
            }
        Show.create_new_show(data)
        return redirect('/dashboard')
    else:
        return redirect('/shows/new')
# Create show

@app.route('/shows/<int:show_id>')
def single_show_data(show_id):
    data={
        'id':show_id
    }
    show=Show.get_show_by_id(data)
    return render_template('single_show.html', show=show)
# View single show

@app.route('/shows/<int:show_id>/delete')
def confirm_show_delete(show_id):
    data={
        'id':show_id
        }
    show=Show.get_show_by_id(data)
    if show.creator.id!=session['user_id']:
        return redirect('/dashboard')
    return render_template('confirm_show_delete.html', show=show)
# Prevent unauthorized user from deleting show

@app.route('/shows/<int:show_id>/confirm_delete')
def delete_show(show_id):
    data={
        'id': show_id
    }
    show=Show.get_show_by_id(data)
    if show.creator.id==session['user_id']:
        Show.delete_show(data)
    return redirect('/dashboard')
# Delete single show with confirmation

@app.route('/shows/<int:show_id>/edit')
def edit_show(show_id):
    data={
        'id':show_id
    }
    show=Show.get_show_by_id(data)
    if show.creator.id !=session['user_id']:
        return redirect('/dashboard')
    return render_template('edit_show.html', show=show)
# Edit single show

@app.route('/shows/<int:show_id>/update', methods=['POST'])
def update_show(show_id):
    data={
        'id': show_id
    }
    show=Show.get_show_by_id(data)
    if show.creator.id !=session['user_id']:
        return redirect('/dashboard')
    if Show.validate_show(request.form):
        data={
            'name':request.form['show_name'],
            'date':request.form['show_date'],
            'description':request.form['show_description'],
            'id':show_id
        }
        Show.update_show(data)
        return redirect(f'/shows/{show_id}')

    else:
        return redirect(f'/shows/{show_id}/edit')
