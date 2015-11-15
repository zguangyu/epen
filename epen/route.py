import os
import pymongo
from flask import render_template, send_from_directory, request, flash, \
    redirect, url_for
from flask.ext.login import login_required
from .app import app, mongo
from .user import User
from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    '''
    Check if the "next" url is in the same host.
    '''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.before_request
def csrf_protect():
    '''
    Check CSRF token before request.
    '''
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

@app.route("/")
def index():
    '''
    The home page. Maybe this should be merged with the post_page function.
    '''
    res = mongo.db.posts.find().sort("time", pymongo.DESCENDING)
    pages = res.count() // 10 + 1
    next = 2 if pages > 1 else None
    return render_template("index.html", posts=res[:10], next=next, pages=pages, page=1)

@app.route("/page/<int:page>/")
def post_page(page):
    '''
    List posts. Each page has 10 posts by default.
    '''
    res = mongo.db.posts.find().sort("time", pymongo.DESCENDING)
    pages = res.count() // 10 + 1
    next = page + 1 if pages > page else None
    previous = page - 1 if page > 1 else None
    return render_template("index.html", posts=res[(page-1)*10:page*10], next=next, previous=previous, pages=pages)

@app.route("/assets/<path:filename>")
def assets(filename):
    '''
    A custom static file router. We need to find the correct location depending
    on the THEME config variable.
    '''
    return send_from_directory(os.path.join(os.path.dirname(__file__), "../themes/%s/assets" % (app.config["THEME"],)), filename)

@app.route("/admin/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("admin/login.html")
    try:
        email = request.form["email"]
        password = request.form["password"]
    except Exception as e:
        flash("Email and password are required.")
        return redirect(url_for("login"))

    user = User.get(email)
    if user is None:
        flash("User not found.")
        return redirect(url_for("login"))

    if not user.authenticate(password):
        flash("Password is incorrect.")
        return redirect(url_for("login"))

    login_user(user)
    return redirect(url_for("admin"))

@app.route("/admin/")
@login_required
def admin():
    return render_template("admin/login.html")
