from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import  InputRequired, Length, AnyOf, Email
from collections import namedtuple

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret'
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'ADifferentSecret'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdOUOsUAAAAALO7K4Gy7nuxO3hMt2xDwvF7FM1r'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdOUOsUAAAAAK4LxfP0CgQUPOUAaYDjWD076n_M'





class TelephoneForm(Form):
    country_code = IntegerField('county code')
    area_code = IntegerField('area code')
    number = StringField('number')

class YearForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')


class LoginForm(FlaskForm):
    username = StringField('Your Username', validators=[InputRequired('A username is required'), Length(min=4, max=8, message='Must be between 4 and 8 characters')])
    password = PasswordField('password', validators=[InputRequired('Password is required'), AnyOf(values=['secret', 'password'])])
    age = IntegerField('age', default=24)
    true = BooleanField('Click here')
    email = StringField('email', validators=[Email()])
    home_phone = FormField(TelephoneForm)
    mobile_phone = FormField(TelephoneForm)
    years = FieldList(FormField(YearForm))

    recaptcha = RecaptchaField()


class NameForm(LoginForm):
    first_name = StringField('first name')
    last_name = StringField('last name')

class TelephoneForm(Form):
    country_code = IntegerField('county code')
    area_code = IntegerField('area code')
    number = StringField('number')

class User:
    def __init__(self , username, age, email):
        self.username = username
        self.age = age
        self.email = email

@app.route('/', methods=['GET', 'POST'])
def index():
    my_user = User('JohnDoe', 58, 'john@doe.com')

    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2005, 1000)
    g2 = group(2006, 1500)
    g3 = group(2007, 1700)


    years = {'years' : [g1, g2, g3]}

    form = NameForm(obj=my_user, data=years)

    del form.mobile_phone

    if form.validate_on_submit():
        # return '<h1>Username: {} Password: {} Age: {} True: {} Email {}</h1>'.format(form.username.data, form.password.data, form.age.data, form.true.data, form.email.data)
        # return '<h1>Country Code: {}, Area code: {}, Number: {}<h1>'.format(form.mobile_phone.country_code.data, form.home_phone.area_code.data, form.home_phone.number.data)
        output = '<h1>'
        for f in form.years:
            output += 'Year: {}'.format(f.year.data)
            output += 'Total: {} <br>'.format(f.total.data)

        output += '</h>'

        return output
    return render_template('index.html', form=form)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('name')

    names = ['middle_name', 'last_name', 'nickname', 'maiden_name']
    for name in names:
        setattr(DynamicForm, name, StringField(name))
    form = DynamicForm()

    if form.validate_on_submit():
        return '<h1>Form has been validated. Name: {}</h1>'.format(form.name.data)
    return render_template('dynamic.html', form=form, names=names)

if __name__ == '__main__':
    app.run(debug=True)



