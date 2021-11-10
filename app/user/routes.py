from app import app

from app.user.models import User


@app.route('/user/signup', methods=['POST'])
def signup():
    user = User()
    return user.signup()


@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login_user():
    user = User()
    return user.login()