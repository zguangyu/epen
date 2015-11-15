import datetime
import random
import hashlib
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .app import app, mongo
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "epen.route.login"

class User(UserMixin):
    '''
    The user class for authentication and querying user profile. This class is
    used for Flask-Login.

    User document fields:

    email (unique)
        User email.

    password
        User password, hashed with werkzeug.security.generate_password_hash.

    is_active
        This property is False by default, until the user activates his account
        from the email.

    activaion_key
        The key to activate the user.

    created_at
        The time when created.

    expire_at
        delete the user after 1 hour without activating.

    name
        The nick name of the user which will be displayed under his post.

    '''
    def __init__(self, user_doc):
        self.doc = user_doc

    @property
    def is_active(self):
        return self.doc.get("is_active")

    @property
    def is_authenticated(self):
        '''
        Temporally useless.
        '''
        return True

    @property
    def get_id(self):
        return self.doc.get("_id")

    @classmethod
    def get(cls, user_email):
        user_doc = mongo.db.users.find_one({"email": user_email})
        if user_doc is None:
            return None
        return cls(user_doc)

    @classmethod
    def create(cls, user_email, password):
        if cls.get(user_email) is not None:
            return None
        now = datetime.datetime.now()
        doc = {
            "email": user_email,
            "password": generate_password_hash(password),
            "is_active": False,
            "created_at": now,
            "expire_at": now + datetime.timedelta(seconds=3600),
            "activation_key": cls.generate_activation_key(user_email),
        }
        result = mongo.db.users.insert_one(doc)
        doc["_id"] = result.inserted_id
        return cls(doc)

    def authenticate(self, password):
        my_pw_hash = self.doc.get("password")
        return check_password_hash(my_pw_hash, password)

    @staticmethod
    def generate_activation_key(user_email):
        salt = hashlib.sha256(str(random.random())).hexdigest()[:5]
        return hashlib.sha256((salt+email).encode("utf-8")).hexdigest()

    def save(self):
        mongo.db.users.find_one_and_replace({"_id": self.doc.get("_id")}, self.doc)

    def activate(self):
        if self.doc["is_active"]:
            return
        self.doc["is_active"] = True
        # None checking is needed, although it must not be None.
        mongo.db.users.find_one_and_update(
            {"_id": self.doc.get("_id")},
            {
                "$set": {"is_active": True},
                "$unset": {"expire_at": ""}
            })

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
