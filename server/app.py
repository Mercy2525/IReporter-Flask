# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ireporter.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ... Define your models, routes, and other components

if __name__ == "__main__":
    app.run()
