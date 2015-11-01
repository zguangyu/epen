import datetime
import babel.dates
from .app import app

def format_datetime(value, format="yyyy-MM-dd"):
    return babel.dates.format_datetime(value, format)

app.jinja_env.filters["datetime"] = format_datetime

def register_blog():
    blog = {}
    blog["title"] = app.config["BLOG_TITLE"]
    blog["date"] = datetime.datetime.now()
    app.jinja_env.globals["blog"] = blog

register_blog()
