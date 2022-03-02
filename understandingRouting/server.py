from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/Dojo')
def dojo():
    return 'Dojo!'

@app.route('/say/<name>')
def say(name):
    print(name)
    return "Hi, " + str(name)

@app.route('/repeat/<number>/<phrase>')

def mention(number, phrase):
    print(phrase)
    return int(number)*str(phrase)

if __name__ == "__main__":
    app.run(debug=True)