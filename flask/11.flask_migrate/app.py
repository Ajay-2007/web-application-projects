from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql3334276:6iIEID8nUa@sql3.freemysqlhosting.net/sql3334276'
    # 'sqlite:///database.db'
app.config['DEBUG'] = True

db = SQLAlchemy(app)
mirate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    subscribed = db.Column(db.Boolean)

class Orderss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)