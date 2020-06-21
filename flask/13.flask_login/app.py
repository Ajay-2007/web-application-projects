from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, fresh_login_required
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse, urljoin
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=4000000)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You can\'t access that page. You need to login first.'
login_manager.fresh_view = 'login'
login_manager.needs_refresh_message = 'You need to login again'

db = SQLAlchemy(app)

serializer = URLSafeTimedSerializer(app.secret_key)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))

    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    session_token = db.Column(db.String(100), unique=True)

    def get_id(self):
        return self.session_token.encode('utf-8')
        # unicode(self.session_token)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if not user:
            return '<h1>User does not exist</h1>'

        login_user(user, remember=True)

        if 'next' in session:
            next = session['next']
            if is_safe_url(next) and next is not None:
                return redirect(next)

        return '<h1>You are now logged in</h1>'

    session['next'] = request.args.get('next')
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return '<h1>You are in the protected area {}<h1>'.format(current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '<h1>You are now logged out</h1> '


@app.route('/fresh')
@fresh_login_required
def fresh():
    return '<h1>You have a fresh session</h1>'

if __name__ == '__main__':
    app.run(debug=True)