from .app import app, mongo


def create_indexes():
    mongo.db.users.create_index("expire_at", expireAfterSeconds=0)

with app.app_context():
    if "users" not in mongo.db.collection_names():
        mongo.db.create_collection("users")
    if not mongo.db.users.list_indexes().alive:
        create_indexex()
