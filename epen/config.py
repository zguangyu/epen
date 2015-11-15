# The default locale to use if no locale selector is registered. This
# defaults to 'en'.
BABEL_DEFAULT_LOCALE = "zh-hans"

# The timezone to use for user facing dates. This defaults to 'UTC' which
# also is the timezone your application must use internally.
BABEL_DEFAULT_TIMEZONE = "Asia/Shanghai"

# The theme to use for the blog. Themes are located at the themes directory,
# each one in a subdirectory.
THEME = "casper"

# The title of your blog.
BLOG_TITLE = "Test Blog"

# Description of your blog. This will also be placed into a meta tag in the
# head section.
BLOG_DESCRIPTION = "An empty blog"

# The database name to make available as the db attribute. Default: app.name.
MONGO_DBNAME = "epen"

# The host name or IP address of your MongoDB server. Default: “localhost”.
MONGO_HOST = "localhost"

# The port number of your MongoDB server. Default: 27017.
MONGO_PORT = "27017"

# The user name for mongodb authentication. Default: None
MONGO_USERNAME = None

# The password for mongodb authentication. Default: None
MONGO_PASSWORD = None

# The secret key used by session and csrf. Please set it in your config_local.py
# and keep it secret.
SECRET_KEY = "blah blah"

from .config_local import *
