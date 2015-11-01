import os
import pymongo
from flask import render_template, send_from_directory
from .app import app, mongo

@app.route("/")
def index():
    res = mongo.db.posts.find().sort("time", pymongo.DESCENDING)
    pages = res.count() // 10 + 1
    next = 2 if pages > 1 else None
    return render_template("index.html", posts=res[:10], next=next, pages=pages, page=1)

@app.route("/page/<int:page>/")
def post_page(page):
    res = mongo.db.posts.find().sort("time", pymongo.DESCENDING)
    pages = res.count() // 10 + 1
    next = page + 1 if pages > page else None
    previous = page - 1 if page > 1 else None
    return render_template("index.html", posts=res[(page-1)*10:page*10], next=next, previous=previous, pages=pages)

@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "../themes/%s/assets" % (app.config["THEME"],)), filename)
