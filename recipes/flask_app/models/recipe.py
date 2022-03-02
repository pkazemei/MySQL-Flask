from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
DB = 'recipes'


class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator = None

    @classmethod
    def create_new_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under30, creator_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under30)s, %(creator_id)s);"
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id=users.id;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        for item in results:
            new_recipe = cls(item)
            new_user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            new_user = User(new_user_data)
            new_recipe.creator = new_user
            recipes.append(new_recipe)
        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.creator_id=users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        recipe = cls(result[0])
        new_user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        new_user = User(new_user_data)
        recipe.creator = new_user
        return recipe

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s;"
        connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name= %(name)s, date=%(date)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s WHERE id= %(id)s;"
        connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters long")
        if len(data['description']) < 3:
            is_valid = False
            flash("Recipe description must be at least 3 characters long")
        if len(data['instructions']) < 3:
            is_valid = False
            flash("Recipe instructions must be at least 3 characters long")
        if len(data['date']) < 8:
            is_valid = False
            flash("Recipe date is invalid")
        return is_valid