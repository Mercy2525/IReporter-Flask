from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import RedFlagRecord, User, db, InterventionRecord, Admin
from flask_migrate import Migrate
import os
# from dotenv import load_dotenv


# load_dotenv()
app = Flask(__name__)
CORS(app,support_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key=os.environ['SECRET_KEY']
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
    
    #signup route
class SignupUser(Resource):
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

            session['user_id']=new_user.id

            return new_user.to_dict(), 201
        return {"error": "user details must be added"}, 422
    
    # login route
class LoginUser(Resource):
    def post(self):
        email  = request.get_json().get('email')
        password = request.get_json().get("password")
        user = User.query.filter(User.email == email).first()
        if user and user.authenticate(password):
            session['user_id']=user.id
            return user.to_dict(),201
        else:
            return {"error":"username or password is incorrect"},401
        
class AddAdmin(Resource):
    def post(self):
        data = request.get_json()

        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
       

        if full_name and username and password:
            new_admin = Admin(full_name=full_name, username=username)
            new_admin.password_hash = password

            db.session.add(new_admin)
            db.session.commit()

            session['admin_id']=new_admin.id

            return make_response(jsonify(new_admin.to_dict()), 201)
        
        return {"error": "user details must be added"}, 422
    
    # login route
class LoginAdmin(Resource):
    def post(self):
        username  = request.get_json().get('username')
        password = request.get_json().get("password")

        admin = Admin.query.filter(Admin.username == username).first()
        if admin and admin.authenticate(password):
            session['admin_id']=admin.id
            return make_response(jsonify(admin.to_dict()),201)
        else:
            return {"error":"username or password is incorrect"},401


class Logout(Resource):
    def delete(self):
        if session.get('user_id') or session.get('admin_id'):
            session['user_id']=None
            session['admin_id']=None
            return {"message": "User logged out successfully"}
        else:
            return {"error":"User must be logged in to logout"}



class CheckSession(Resource):
    def get(self):
        if session['user_id'] or session['admin_id']:
            return {"message": "user in session"}
        else:
            return {"error": "user not in session:please signin/login"}


     
    #  all users route
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users),200) 

    #  all admins route
class AdminResource(Resource):
    def get(self):
        admins = [admin.to_dict() for admin in Admin.query.all()]
       
        return make_response(jsonify(admins),200)
    

    # redflag records route
class RedFlagRecordResource(Resource):
    def get(self):
        red_flags = [red_flag.to_dict() for red_flag in RedFlagRecord.query.all()]
        
        return make_response(jsonify(red_flags),200)
   
        # post redflag records
    def post(self):
        data = request.get_json()

        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')
       
        if image and video and location and status:
            new_redflag = RedFlagRecord(image=image, video=video, location=location, status=status, user_id=user_id)

            db.session.add(new_redflag)
            db.session.commit()

            return make_response(new_redflag.to_dict(), 201) 
        return {"error": "RedFlag details must be added"}, 422
    
class RedFlagRecordById(Resource):

    #get red-flag by id
    def get(self,id):
        pass
        red_flag=RedFlagRecord.query.filter_by(id=id).first().to_dict()

        return make_response(jsonify(red_flag),200)
    
        # edit a red-flag record    
    def patch(self,id):
        redflag = RedFlagRecord.query.filter_by(id=id).first()

        if redflag:
            for attr in request.get_json():
                setattr(redflag,attr, request.get_json()[attr])

            db.session.add(redflag)
            db.session.commit()
            
            return make_response(jsonify(redflag.to_dict(), 200))
        
        return {"error": "Red-flag record not found"}, 404

        # delete a red-flag record
    def delete(self,id):
        red_flag=RedFlagRecord.query.get(id)

        if red_flag:
            db.session.delete(red_flag)
            db.session.commit()
            return {"message": "Red-flag record deleted successfully"}, 200
        else:
            return {"error": "Red-flag record not found"}, 404
        
    
    # intervention records route
class InterventionRecordResource(Resource):

        # get all intervention records
    def get(self):
        
        intervention_flags = [intervention.to_dict() for  intervention in InterventionRecord.query.all()]
        
        return make_response(jsonify(intervention_flags),200)

        # post an intervention record
    def post(self):
        data = request.get_json()

        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')

        if image and video and location:
            new_intervention = InterventionRecord(image=image, video=video, location=location, status=status, user_id=user_id)

            db.session.add(new_intervention)
            db.session.commit()
      
            return make_response(jsonify(new_intervention.to_dict(), 201))
        
        return {"error": "Intervention details must be added"}, 422
    
class InterventionRecordById(Resource):
    def get(self,id):
        record=InterventionRecord.query.get(id)

        return make_response(jsonify(record),200)
    
        # edit an intervention record
    def patch(self, id):
        intervention = InterventionRecord.query.filter_by(id=id).first()

        if intervention:
            for attr in request.get_json():
                setattr(intervention,attr,request.get_json()[attr])

                db.session.add(intervention)
                db.session.commit()
            return make_response(jsonify(intervention.to_dict(), 200)) 
        
        
        return {"error": "Intervention record not found"}, 404


        # delete an intervention record
    def delete(self, id):
        intervention = InterventionRecord.query.filter_by(id=id).first()

        if intervention:
            db.session.delete(intervention)
            db.session.commit()
            return {"message": "Intervention record deleted successfully"}, 200
        else:
            return {"error": "Intervention record not found"}, 404



api.add_resource(Index,'/', endpoint='landing')
api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(AdminResource, '/admins', endpoint='admins')
api.add_resource(RedFlagRecordResource, '/redflags', endpoint='redflags')
api.add_resource(RedFlagRecordById,'/redflags/<int:id>', endpoint='redflags_id')
api.add_resource(InterventionRecordResource, '/intervention', endpoint='intervention')
api.add_resource(InterventionRecordById, '/intervention/<int:id>', endpoint='interventbyid')
api.add_resource(SignupUser, '/signup_user', endpoint='signup')
api.add_resource(LoginUser, '/login_user', endpoint='login')
api.add_resource(AddAdmin, '/add_admin', endpoint='add_admin')
api.add_resource(LoginAdmin, '/login_admin', endpoint='login_admin')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession,'/session',endpoint='session' )




if __name__ == '__main__':
    app.run(port=5555, debug=True)

