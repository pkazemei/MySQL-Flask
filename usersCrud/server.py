# Import route file from destination folder

from flask_app.controllers import users_routes
from flask_app import app

# server.py collects controllers with import statements

if __name__ == '__main__':
    app.run(debug = True)