from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
DB = 'login_and_registration'

import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s;"
        result=connectToMySQL(DB).query_db(query, data)

        if len(result) == 0:
            return None
        else:
            return cls(result[0])

    @classmethod
    def create_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result=connectToMySQL(DB).query_db(query, data)

    @staticmethod
    def validate_new_user(data):
        is_valid = True

        if len(data['first_name']) < 3 or len(data['first_name']) > 32:
            is_valid = False
            flash("First Name should be 3 to 32 characters in length")

        if len(data['last_name']) < 3 or len(data['last_name']) > 32:
            is_valid = False
            flash("Last Name should be 3 to 32 characters in length")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Provide a valid email address")
        elif User.get_user_by_email(data) != None:
                is_valid=False
                flash(f"Email is already in use")

        if len(data['password'])<8:
            is_valid=False
            flash("Password should be at least 8 characters in length")

        if data['password']!=data['confirm_password']:
            is_valid=False
            flash("Password does not match")

        return is_valid