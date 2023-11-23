from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource, reqparse
from models import RedFlagRecord, User, db, InterventionRecord, Admin
from flask_migrate import Migrate


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
class SignupResource(Resource):
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
class LoginResource(Resource):
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
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users)) 

    #  all admins route
class AdminResource(Resource):
    def get(self):
        admins = Admin.query.all()
        admin_list = [{"id": admin.id, "full_name": admin.full_name, "username": admin.username} for admin in admins]
        return jsonify(users=admin_list)
    

    # redflag records route
class RedFlagRecordResource(Resource):
    def get(self):
        red_flags = [red_flag.to_dict() for red_flag in RedFlagRecord.query.all()]
        
        return make_response( jsonify(red_flags),200)
   
        # post redflag records
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
    
        # edit a red-flag record    
    def put(self, redflag_id):
        data = request.get_json()
        redflag = RedFlagRecord.query.get(redflag_id)

        if redflag:
            redflag.image = data.get('image', redflag.image)
            redflag.video = data.get('video', redflag.video)
            redflag.location = data.get('location', redflag.location)
            redflag.status = data.get('status', redflag.status)

            db.session.commit()
            return redflag.to_dict(), 200
        else:
            return {"error": "Red-flag record not found"}, 404

        # delete a red-flag record
    def delete(self, redflag_id):
        redflag = RedFlagRecord.query.get(redflag_id)

        if redflag:
            db.session.delete(redflag)
            db.session.commit()
            return {"message": "Red-flag record deleted successfully"}, 200
        else:
            return {"error": "Red-flag record not found"}, 404
        
    
    # intervention records route
class InterventionRecordResource(Resource):

        # get all intervention records
    def get(self):
        user_id = session.get('user_id') 
        intervention_flags = InterventionRecord.query.filter_by(user_id=user_id).all()
        intervention_data = [{'id': intervention.id, 'image': intervention.image, 'video': intervention.video,
                              'location': intervention.location, 'status': intervention.status,
                              'created_at': intervention.created_at, 'updated_at': intervention.updated_at}
                             for intervention in intervention_flags]
        return jsonify({'intervention_flags': intervention_data})

        # post an intervention record
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
    
        # edit an intervention record
    def put(self, intervention_id):
        data = request.get_json()
        intervention = InterventionRecord.query.get(intervention_id)

        if intervention:
            intervention.image = data.get('image', intervention.image)
            intervention.video = data.get('video', intervention.video)
            intervention.location = data.get('location', intervention.location)
            intervention.status = data.get('status', intervention.status)

            db.session.commit()
            return intervention.to_dict(), 200
        else:
            return {"error": "Intervention record not found"}, 404


        # delete an intervention record
    def delete(self, intervention_id):
        intervention = InterventionRecord.query.get(intervention_id)

        if intervention:
            db.session.delete(intervention)
            db.session.commit()
            return {"message": "Intervention record deleted successfully"}, 200
        else:
            return {"error": "Intervention record not found"}, 404



api.add_resource(Index,'/', endpoint='landing')
api.add_resource(SignupResource, '/signup', endpoint='signup')
api.add_resource(LoginResource, '/login')


api.add_resource(UserResource, '/users')

api.add_resource(AdminResource, '/admins')
api.add_resource(RedFlagRecordResource, '/redflags')
api.add_resource(RedFlagRecordResource, '/redflags/<int:redflags_id>', endpoint='redflags')
api.add_resource(InterventionRecordResource, '/interventionrecords')
api.add_resource(InterventionRecordResource, '/interventionrecords/<int:intervention_id>', endpoint='interventionrecords')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

