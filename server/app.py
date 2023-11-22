from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource, reqparse
from models import User, RedFlagRecord, db, InterventionRecord, Admin
from flask_migrate import Migrate
import os


app = Flask(__name__)
CORS(app,support_credentials=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
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
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if full_name and username and email and password:
            new_user = User(full_name=full_name, username=username, email=email)
            new_user.password_hash = password
            db.session.add(new_user)
            db.session.commit()
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
        admins = Admin.query.all()
        admin_list = [{"id": admin.id, "full_name": admin.full_name, "username": admin.username} for admin in admins]
        return jsonify(users=admin_list)
    
    
    # redflag records route
class RedFlagRecord(Resource):
    def get(self):
        red_flags = RedFlagRecord.query.filter_by(user_id=User.id).all()
        red_flags_data = [{'id': redflag.id, 'image': redflag.image, 'video': redflag.video,
                           'location': redflag.location, 'status': redflag.status, 'created_at': redflag.created_at, 'updated_at': redflag.updated_at} for redflag in red_flags]
        return jsonify({'red_flags': red_flags_data})
   
    def post(self):
        data = request.get_json()
        image = data.get('image')
        video = data.get('video')
        location = data.get(' location')
        status = data.get('status')
       
        if image and video and location and status:
            new_redflag = RedFlagRecord(image=image, video=video, location=location, status=status)
            db.session.add(new_redflag)
            db.session.commit()
            session['user_id'] = new_redflag.id
            return new_redflag.to_dict(), 201
        return {"error": "RedFlag details must be added"}, 422
    
    # intervention records route
class InterventionRecord(Resource):
    def get(self):
        intervention_flags = InterventionRecord.query.filter_by(user_id=User.id).all()
        intervention_data = [{'id': intervention.id, 'image': intervention.image, 'video': intervention.video,
                           'location': intervention.location, 'status': intervention.status, 'created_at': intervention.created_at, 'updated_at': intervention.updated_at} for intervention in intervention_flags]
        return jsonify({'intervention_flags': intervention_data})
   
    def post(self):
        data = request.get_json()
        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
       
        if image and video and location:
            new_intervention = InterventionRecord(image=image, video=video, location=location, status=status)
            db.session.add(new_intervention)
            db.session.commit()
            session['user_id'] = new_intervention.id
            return new_intervention.to_dict(), 201
        return {"error": "Intervention details must be added"}, 422



api.add_resource(Index,'/', endpoint='landing')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(User, '/users')
api.add_resource(RedFlagRecord, '/redflags')
api.add_resource(InterventionRecord, '/interventionrecords')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

