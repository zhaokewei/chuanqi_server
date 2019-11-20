from exts import db
from sqlalchemy import text, func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, default="", index=True)
    phone = db.Column(db.String(255), unique=True, default="", index=True)
    email = db.Column(db.String(255), unique=True, default="", index=True)
    password = db.Column(db.String(255), default="")
    info = db.Column(db.Text(), default="")
    avatar_url = db.Column(db.String(1024), default="")
    gender = db.Column(db.SmallInteger(), default=-1)
    status = db.Column(db.SmallInteger(), default=0, index=True)
    create_time = db.Column(db.DateTime(), server_default=func.now())
    update_time = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")

