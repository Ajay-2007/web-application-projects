from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, ValidationError
     # , DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import  InputRequired, Length, AnyOf
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdOUOsUAAAAALO7K4Gy7nuxO3hMt2xDwvF7FM1r'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdOUOsUAAAAAK4LxfP0CgQUPOUAaYDjWD076n_M'
app.config['TESTING'] = True
bootstrap = Bootstrap(app)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required'), Length(min=4, max=8, message='Must be between 4 and 8 characters')])
    password = PasswordField('password', validators=[InputRequired('Password is required'), AnyOf(values=['secret', 'password'])])
    entrydate = DateField('entrydate', format='%Y-%m-%d')

    def validate_username(form, field):
        if field.data != 'Anthony':
            raise ValidationError('You do not have the right username')

    recaptcha = RecaptchaField()

@app.route('/index', methods=['GET', 'POST'])
def index():

    form = LoginForm()

    user = User(username='Anthony', password='password')
    print(user.username)
    print(user.password)
    if form.validate_on_submit():

        form.populate_obj(user)
        print(user.username)
        print(user.password)
        return '<h1>Username: {} Password: {} Date: {}</h1>'.format(form.username.data, form.password.data, form.entrydate.data)


    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)



