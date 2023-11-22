from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource, reqparse
from models import User, RedFlagRecord, db
from flask_migrate import Migrate
import os


app = Flask(__name__)
CORS(app,support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

    # home route
class Index(Resource):
    def get(self):
        response_body = '<h1>Hello World</h1>'
        status = 200
        headers = {}
        return make_response(response_body,status,headers)
    
    # signup route
class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if username and email and password:
            new_user = User(username=username, email=email)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return new_user.to_dict(), 201
        return {"error": "user details must be added"}, 422
    
    # login route
class Login(Resource):
    def post(self):
        email  = request.get_json().get('email')
        password = request.get_json().get("password")
        user = User.query.filter(User.email == email).first()
        if user and user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(),201
        else:
            return {"error":"username or password is incorrect"},401

    #  all users route
class User(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{"id": user.id, "username": user.username, "email": user.email, "full_name": user.full_name } for user in users]
        return jsonify(users=user_list)

    #  all admins route
class Admin(Resource):
    def get(self):
        admins = User.query.all()
        admin_list = [{"id": admin.id, "username": admin.username, "email": admin.email, "full_name": admin.full_name } for admin in admins]
        return jsonify(users=admin_list)
    

    # redflag route
class RedFlag(Resource):
    def get(self):
        red_flags = RedFlagRecord.query.filter_by(user_id=User.id).all()
        red_flags_data = [{'id': redflag.id, 'title': redflag.title, 'description': redflag.description,
                           'author': redflag.author} for redflag in red_flags]
        return jsonify({'red_flags': red_flags_data})
   
    def post(self):
        data = request.get_json()
        title = data.get('title')
        username = data.get('description')
        author = data.get(' author')
       
        if title and username and author:
            new_redflag = RedFlag(title=title, username=username, author=author)
            db.session.add(new_redflag)
            db.session.commit()
            session['user_id'] = new_redflag.id
            return new_redflag.to_dict(), 201
        return {"error": "RedFlag details must be added"}, 422



api.add_resource(Index,'/', endpoint='landing')
api.add_resource(Signup, '/api/signup')
api.add_resource(Login, '/api/login')
api.add_resource(User, '/users')
api.add_resource(RedFlag, '/api/redflags')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
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
