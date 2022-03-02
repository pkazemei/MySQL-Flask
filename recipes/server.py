from flask_app import app
from flask_app.controllers import recipes, users
# import controller files here

if __name__ == '__main__':
    app.run(debug = True)