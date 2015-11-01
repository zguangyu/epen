from epen import app
from flask.ext.script import Manager

app.debug = True
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
