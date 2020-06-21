from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # 'sqlite:///database.db'
app.config['DEBUG'] = True

db = SQLAlchemy(app)
mirate = Migrate(app, db)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # location = db.Column(db.String(50))


if __name__ == '__main__':
    app.run(debug=True)