from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeSerializer


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_auto_expire.db'
app.config['SECRET_KEY'] = 'thisissecret'
app.config['MONGO_URI'] = 'mongodb+srv://d33ps3curity:d33ps3curity@cluster0-st61f.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)
login_manager = LoginManager(app)
serializer = URLSafeSerializer(app.secret_key)


class Member(UserMixin):

    def __init__(self, member_data):
        self.member_data = member_data

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.member_data['session_token']

@login_manager.user_loader
def load_user(session_token):
    members = mongo.db.members
    member_data = members.find_one({'session_token' : session_token})

    if member_data:
        return Member(member_data)
    return None

@app.route('/create')
def create():
    members = mongo.db.members
    session_token = serializer.dumps(['Anthony', 'password'])
    members.insert({'name' : 'Anthony', 'session_token' : session_token})
    return '<h1>User Created</h1>'


@app.route('/login')
def index():
    members = mongo.db.members
    member = members.find_one({'name' : 'Anthony'})
    # validation stuff
    anthony = Member(member)
    login_user(anthony)
    return '<h1>You are now logged in!</h1>'


@app.route('/home')
@login_required
def home():
    return '<h1>The current user is {}</h1>'.format(current_user.member_data['name'])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'

# @app.route('/home')
# @login_required
# def home():
#     return 'The current user is ' + current_user.username

if __name__ == '__main__':
    app.run(debug=True)