from flask_app.config.mysqlconnection import connectToMySQL
DB='users_schema'

class User:
    # User information extracted from the database
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# create
    @classmethod
    def create_new_user(cls, data):
        # Use old python syntax to insert variables
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s);"

        # Insert schema into this
        result = connectToMySQL(DB).query_db(query, data)
        return result

# read
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"

        result=connectToMySQL(DB).query_db(query)
        all_users=[]
        for user in result:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM users WHERE ID= %(id)s"
        result=connectToMySQL(DB).query_db(query, data)
        return result[0]

# update
    @classmethod
    def update_user(cls, data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        result=connectToMySQL(DB).query_db(query, data)

# destroy
    @classmethod
    def destroy_user(cls, data):
        query="DELETE FROM users WHERE id=%(id)s"
        result=connectToMySQL(DB).query_db(query, data)