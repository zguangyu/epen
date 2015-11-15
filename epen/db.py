from .app import app, mongo


def create_indexes():
    mongo.db.users.create_index("expire_at", expireAfterSeconds=0)

if not mongo.db.users.list_indexes().alive:
    create_indexex()
