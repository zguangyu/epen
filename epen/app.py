from flask import Flask
from flask.ext.pymongo import PyMongo
from jinja2 import FileSystemLoader

app = Flask("epen")
app.config.from_pyfile("config.py")
app.jinja_loader = FileSystemLoader("themes/%s" % (app.config["THEME"],))

mongo = PyMongo(app)
