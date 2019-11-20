from flask import Flask, Blueprint
from flask_login import login_required, UserMixin, login_user, logout_user
from config import *
from exts import db, login_manager
from models import *


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    app.secret_key = SECRET_KEY
    login_manager.init_app(app)

    return app


app = create_app()


class UserForAuth(UserMixin):
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return '1'


@app.route('/')
def hello_world():
    return 'Hello World!'


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    user = UserForAuth()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return {
        "code": -1,
        "msg": '请登录'
    }


@auth.route('login', methods=['GET', 'POST'])
def login():
    user = User()
    login_user(user)
    return 'login page'


@auth.route('logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return 'logout page'


@app.route('/test')
@login_required
def test():
    return 'yes you are allowed'




app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run()
