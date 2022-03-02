from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
DB = 'final_prep'


class Show():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator = None

    @classmethod
    def create_new_show(cls, data):
        query = "INSERT INTO shows (name, description, date, creator_id) VALUES (%(name)s, %(description)s, %(date)s, %(creator_id)s);"
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows JOIN users ON shows.creator_id=users.id;"
        results = connectToMySQL(DB).query_db(query)
        shows = []
        for item in results:
            new_show = cls(item)
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
            new_show.creator = new_user
            shows.append(new_show)
        return shows

    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.creator_id=users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        show = cls(result[0])
        new_user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        new_user=User(new_user_data)
        show.creator=new_user
        return show

    @classmethod
    def delete_show(cls, data):
        query="DELETE FROM shows WHERE id=%(id)s;"
        connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def update_show(cls, data):
        query="UPDATE shows SET name= %(name)s, date=%(date)s, description=%(description)s WHERE id= %(id)s;"
        connectToMySQL(DB).query_db(query, data)
    
    @staticmethod
    def validate_show(data):
        is_valid = True
        if len(data['show_name']) < 1 or len(data['show_name']) > 100:
            is_valid = False
            flash("Show name should be 1 to 100 characters")
        if len(data['show_date']) != 10:
            is_valid = False
            flash("Provide a valid date (MM/DD/YYYY)")
        if len(data['show_description']) < 1 or len(data['show_description']) > 500:
            is_valid = False
            flash("Show description should be 1 to 500 characters")
        return is_valid
