from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/<name>') # decorator this is url endpoint
def index(name):
    return '<h1>Hello {}</h1>'.format(name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name' : 'Default'})
@app.route('/home/<string:name>', methods=['GET', 'POST'])
def home(name):
    return '<h1>Hello {}, You are on the home page</h1>'.format(name)

@app.route('/json')
def json():
    return jsonify({'key1' : 'value1', 'key2': [1, 2, 3]})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page</h1>'.format(name, location)
@app.route('/theform')
def theform():
    return '''<form method="POST" action="/process">
              <input type="text" name="name">
              <input type="text" name="location">
              <input type="submit">
              </form>'''
if __name__ == '__main__':
    app.run(debug=True)