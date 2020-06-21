from flask import Flask
from flask import jsonify
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from flask import render_template
import sqlite3
from flask import g

app = Flask(__name__)

# Using flask configuration
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    sql = sqlite3.connect('C:\\Users\\d33ps3curity\\Downloads\\data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/<name>') # decorator this is url endpoint
def index(name):
    session.pop('name', None)
    return '<h1>Hello {}</h1>'.format(name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return render_template('home.html', name=name, display=True, mylist=['one', 'two', 'three', 'four'],
                           listofdictionaries = [{'name': 'Zach'}, {'name': 'Zoe'}], results=results)

@app.route('/json')
def json():
    if 'name' in session:
    # mylist = [1, 2, 3, 4]
    # name = session['name']
        name = session['name']
    else:
        name = 'NotinSession'
    return jsonify({'key1' : 'value1', 'key2': [1, 2, 3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page</h1>'.format(name, location)

@app.route('/theform', methods=['GET', 'POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()
        #
        # return '<h1>Hello {}. You are from {}. You have successfully submitted the form.</h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location))

'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return '<h1>Hello {}. You are from {}. You have successfully submitted the form.</h1>'.format(name, location)
'''
@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result': 'Success ', 'name': name, 'location': location, 'randomkeyinlist' : randomlist[1]})

# Redirects and url_for
@app.route('/use_redirect_and_url_for', methods=['GET', 'POST'])
def use_redirect_and_url_for():
    if request.method == 'GET':
        return '''<form method="POST" action="/theform">
                          <input type="text" name="name">
                          <input type="text" name="location">
                          <input type="submit" value="Submit">
                          </form>'''

    else:
        redirect(url_for('/home'))


@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}.The location is {}.</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])


if __name__ == '__main__':
    app.run()