import os
from flask import render_template, send_from_directory
from .app import app, mongo

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assets/<path:filename>")
def custom_static(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "../themes/%s/assets" % (app.config["THEME"],)), filename)
