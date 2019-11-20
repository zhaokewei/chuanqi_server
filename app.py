from flask import Flask, Blueprint
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user

app = Flask(__name__)
app.secret_key = 'zhaochuanqi'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


class User(UserMixin):
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
    user = User()
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
