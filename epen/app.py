from flask import Flask
from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
import jinja2

app = Flask("epen")
app.config.from_pyfile("config.py")
_my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader("themes/%s" % (app.config["THEME"],)),
    jinja2.FileSystemLoader("core/"),
])
app.jinja_loader = _my_loader

mongo = PyMongo(app)
