import datetime
import babel.dates
from flask import session
from .app import app

def format_datetime(value, format="yyyy-MM-dd"):
    return babel.dates.format_datetime(value, format)

app.jinja_env.filters["datetime"] = format_datetime

def generate_csrf_token(input=True):
    if "_csrf_token" not in session:
        session["_csrf_token"] = some_random_string()
    if input:
        return "<input name=_csrf_token type=hidden value=\"%s\">" % (session['_csrf_token'],)
    return session[""]

app.jinja_env.globals["csrf_input"] = generate_csrf_token

def register_blog():
    blog = {}
    blog["title"] = app.config["BLOG_TITLE"]
    blog["description"] = app.config["BLOG_DESCRIPTION"]
    blog["date"] = datetime.datetime.now()
    app.jinja_env.globals["blog"] = blog

register_blog()
