from flask import Flask, render_template
import sys

app = Flask(__name__)
app.debug = True

@app.route("/")
def helloworld():
    return render_template("hello.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/list")
def list():
    return render_template("list.html")
