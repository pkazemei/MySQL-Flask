from flask_app import app
from flask import render_template, flash, session, redirect, request
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def exam_dashboard():
    if 'user_id' not in session:
        flash("This page is only available to logged in users")
        return redirect('/')
    data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(data)
    recipes=Recipe.get_all_recipes()
    return render_template('recipes.html', recipes=recipes, user=user)
# Once logged in, takes user to dashboard

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(data)
    return render_template('new_recipe.html', user=user)
# Returns to create recipe screen

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data={
        'name':request.form['name'],
        'date':request.form['date'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'under30':request.form['under30'],
        'creator_id':session['user_id']
        }
    Recipe.create_new_recipe(data)
    return redirect('/dashboard')
# Create recipe

@app.route('/recipes/<int:id>')
def single_recipe_data(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    user_data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(user_data)
    recipe=Recipe.get_recipe_by_id(data)
    return render_template('single_recipe.html', recipe=recipe, user=user)
# View single recipe

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
        }
    Recipe.delete_recipe(data)
    return redirect ('/dashboard')
# Prevent unauthorized user from deleting recipe

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    user_data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(user_data)
    recipe=Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', recipe=recipe, user=user)
# Edit single recipe

@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect ('/recipes/new')

    data={
        'name':request.form['name'],
        'date':request.form['date'],
        'description':request.form['description'],
        'instructions':request.form['instructions'],
        'under30':request.form['under30'],
        'id':id
    }
    Recipe.update_recipe(data)
    return redirect(f'/recipes/{id}')