from flask import Flask, Blueprint, request, jsonify
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


@app.route('/')
def hello_world():
    return 'Hello World!'


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id==user_id).first()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return {
        "code": 401,
        "msg": '请登录'
    }


@auth.route('login', methods=['POST'])
def login():
    try:
        name = request.json.get('username')
        password = request.json.get('password')
    except:
        return jsonify({
            "code": -100,
            "msg": "params not enough"
        })
    print(name, password)
    if name and password:
        user = User.query.filter(User.name==name, User.password==password).first()
        if user:
            login_user(user)
            return jsonify({
                "code": 0,
                "msg": "login success"
            })
    return jsonify({
        "code": -1,
        "msg": "name or password error"
    })


@auth.route('logout', methods=['GET'])
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
