from flask import Flask, render_template, redirect, request
from flask.globals import session
from flask.wrappers import Request
app=Flask(__name__)

app.secret_key = 'keep it unsafe'

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('info.html')

@app.route('/post', methods=["POST"])
def post():
    session["name"]=request.form["name"]
    session["location"]=request.form["location"]
    session["language"]=request.form["language"]
    session["comment"]=request.form["comment"]
    return redirect('/result')

if __name__ == "__main__":
    app.run(debug=True)