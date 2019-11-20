from app import create_app, db
from models import *


def create_tables():
    app = create_app()
    db.create_all(app=app)


def insert_records():
    app = create_app()
    app.app_context().push()
    with app.app_context():
        user = User()
        user.name = 'zhaokewei'
        user.password = '123456'
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    insert_records()