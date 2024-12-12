from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<h1 style="height:100vh; display: flex; justify-content: center; align-items: center">Hello world, with debugger!<h1>'

@app.route("/about")
def about_page():
    return '<h1 style="height:100vh; display: flex; justify-content: center; align-items: center">About!<h1>'