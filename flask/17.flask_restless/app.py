from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



# for performing restapi queries
# http://127.0.0.1:5000/api/user?q={"filters": [{"name":"name", "op": "like", "val": "%e%"}]}
# {"filters": [{"or": [{"name":"name", "op": "like", "val": "%e%"}, {"name": "id", "op": "gt", "val": 1}]}]}
# http://127.0.0.1:5000/api/user?q={"filters": [{"name": "items", "op": "any", "val": {"name": "id", "op": "gt", "val": 3}}]}
# http://127.0.0.1:5000/api/item?q={"filters": [{"name": "id", "op": "gt", "val": 6}]}
manager.create_api(User, methods=['GET', 'POST', 'PUT'])
manager.create_api(Item, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_delete_many=True, allow_patch_many=True)



if __name__ == '__main__':
    app.run(debug=True)