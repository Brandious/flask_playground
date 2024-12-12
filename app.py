from flask import Flask

app = Flask(__name__)

style = "height:100vh; display: flex; justify-content: center; align-items: center"


@app.route("/")
def hello_world():
    return f'<h1 style="{style}">Hello world, with debugger!<h1>'

@app.route("/about/<username>")
def about_page(username):
    return f'<h1 style="{style}">About {username}!<h1>'