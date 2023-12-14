from flask_cors import CORS
from flask import Flask, jsonify, request, session, make_response
from flask_restful import Api, Resource
from models import RedFlagRecord, User, db, InterventionRecord, Admin
from flask_migrate import Migrate
import os
from werkzeug.exceptions import NotFound
from datetime import timedelta
from flask_session import Session
from flask_mail import Mail,Message

# from dotenv import load_dotenv

# load_dotenv()

app = Flask(__name__)
CORS(app,support_credentials=True,)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key=os.environ['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_FILE_DIR'] = 'session_dir'
app.config['JSONIFY_PRETTYPRINT_REGULAR']= True

app.config['MAIL_SERVER']='smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'mercywmuriithi.mm@gmail.com'
app.config['MAIL_PASSWORD'] = '035DD7B03036F704AE4605DDFF792CE01787'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)
Session(app)
mail=Mail(app)



def email_on_signup(user_email):
    message= Message(
        subject='Welcome to IReporter :)',
        recipients=[user_email],
        sender='mercywmuriithi.mm@gmail.com'
    )
    message.body= "Hello Citizen X, \n\n Welcome to IReporter,let's make our country corruption free \n\n Thank you"
    print(message.body)

    mail.send(message)

def email_on_status_change(user_email,title,status):
    message= Message(
        subject='Status Update',
        recipients=[user_email],
        sender='mercywmuriithi.mm@gmail.com'
    )


    if status == 'resolved':
        message.body= f"Hello Citizen X, \n\n We are happy to notify that your report, {title}, has been {status}. You are our valuable contributor, let's fix this country one report at a time \n\n Thank you for your bold contibution."
    elif status == 'rejected':
        message.body= f"Hello Citizen X, \n\n The report, {title}, has been {status}. We have reason to believe the information you have provided is inaccurate and has no concrete proof \n\n Thank you for your bold contibution."
    elif status == 'under investigation':
        message.body= f"Hello Citizen X, \n\n Your report, {title}, is {status}. We have found your claims concrete and we proceed to look into it,we'll keep you posted. \n\n Thank you for your bold contibution."

    print(message.body)
    print('email works')

    mail.send(message)
   

    #home route
    #
class Index(Resource):
    def get(self):
        response_body = {"message": "Hello World"}
        status = 200
        headers = {}
        return make_response(jsonify(response_body), status, headers)

    
    #signup route
class SignupUser(Resource):
    def post(self):
        data = request.get_json()

        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        

        if full_name and username and email and password:
            new_user = User(full_name=full_name, username=username, email=email)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()


            session['user_id']=new_user.id
            session['user_type'] = 'user'

            email_on_signup(email)


            return make_response(jsonify(new_user.to_dict()),201)
        
        return make_response(jsonify({"error": "user details must be added"}),422)
    
    # login route
class LoginUser(Resource):
    def post(self):
        email  = request.get_json().get('email')
        password = request.get_json().get("password")

        user = User.query.filter(User.email == email).first()

        if user:
            if user.authenticate(password):
                session['user_id']=user.id
                session['user_type'] = 'user'

                return make_response(jsonify(user.to_dict()), 201)
                
            else:
                return make_response(jsonify({"error": "username or password is incorrect"}), 401)
       
        return make_response(jsonify({"error": "User not Registered"}), 404)
            
class CheckUser(Resource):
    def get(self):
        user_type = session.get('user_type')
        if user_type == 'user':
            user = User.query.filter(User.id == session.get('user_id')).first()
            if user:
                return make_response(jsonify(user.to_dict()),200)
            else:
                return make_response(jsonify({"error": "user not in session: please signin/login"}), 401)
        

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id']= None
            session.pop('user_id')
            print('user logged out')
            return make_response(jsonify({"message": "User logged out successfully"}), 200)
        else:
            return make_response(jsonify({"error":"User must be logged in to logout"}),401)
    
   
        
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
            session['user_type'] = 'admin'

            return make_response(jsonify(new_admin.to_dict()), 201)
        
        return make_response(jsonify({"error": "user details must be added"}), 422)
    
    
#     # login route
class LoginAdmin(Resource):
    def post(self):
        username  = request.get_json().get('username')
        password = request.get_json().get("password")

        admin = Admin.query.filter(Admin.username == username).first()

        if admin:
            if admin.authenticate(password):
                session['admin_id']=admin.id
                session['user_type'] = 'admin' 

                return make_response(jsonify(admin.to_dict()),201)
            else:
                return make_response(jsonify({"error":"username or password is incorrect"}),401)
        print("User not registered.") 
        return make_response(jsonify({"error": "User not Registered"}), 404)


class CheckAdmin(Resource):
    def get(self):
        user_type = session.get('user_type')
        if user_type == 'admin':
            admin = Admin.query.filter(Admin.id == session.get('admin_id')).first()
            if admin:
                return make_response(jsonify(admin.to_dict()), 200)
            else:
                return make_response(jsonify({"error": "Admin not in session: please signin/login"}), 401)

        
class LogoutAdmin(Resource):
    def delete(self):
        if session.get('admin_id'):
            session['admin_id']=None
            session.pop('admin_id')
            print('admin logged out')
            return make_response(jsonify({"message": "Admin logged out successfully"}),200)
        else:
            return make_response(jsonify({"error":"Admin must be logged in to logout"}),401)



     
    #  all users route
class UserResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]

        return make_response(jsonify(users),200) 
    
class UserById(Resource):
    def get(self,id):
        users = User.query.filter_by(id=id).first()

        return make_response(jsonify(users.to_dict()),200) 

    #  all admins route
class AdminResource(Resource):
    def get(self):
        admins = [admin.to_dict() for admin in Admin.query.all()]
       
        return make_response(jsonify(admins),200)
    

    # redflag records route
class RedFlagRecordResource(Resource):
    def get(self):
        red_flags = [red_flag.to_dict() for red_flag in RedFlagRecord.query.all()]

        if red_flags:
            return make_response(jsonify(red_flags),200)
        else:
            return make_response(jsonify({"error": "There are no Red-flag records"}), 404)

   
        # post redflag records
    def post(self):
        data = request.get_json()

        title=data.get('title')
        description=data.get('description')
        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')
       
        if title and description and location and status:
            new_redflag = RedFlagRecord( title=title, description= description, image=image, video=video, location=location, status=status, user_id=user_id)
            
            db.session.add(new_redflag)
            db.session.commit()

            return make_response(jsonify(new_redflag.to_dict()), 201) 
        return make_response(jsonify({"error": "RedFlag details must be added"}), 422)
    
class RedFlagRecordById(Resource):

    #get red-flag by id
    def get(self,id):
        pass
        red_flag=RedFlagRecord.query.filter_by(id=id).first().to_dict()

        if red_flag:
            return make_response(jsonify(red_flag),200)
        
        return make_response(jsonify({"error": "Red-flag record not found"}), 404)
    
        # edit a red-flag record    
    def patch(self,id):
        redflag = RedFlagRecord.query.filter_by(id=id).first()
        data = request.get_json()

        if redflag:
            for attr in request.get_json():
                setattr(redflag,attr, request.get_json()[attr])

            db.session.add(redflag)
            db.session.commit()

            user = User.query.get(redflag.user_id)
            if user:
                email_on_status_change(user.email,redflag.title,redflag.status)
            
            return make_response(jsonify(redflag.to_dict()), 200)
        
        return make_response(jsonify({"error": "Red-flag record not found"}), 404)

        # delete a red-flag record
    def delete(self,id):
        red_flag=RedFlagRecord.query.get(id)

        if red_flag:
            db.session.delete(red_flag)
            db.session.commit()
            return make_response(jsonify({"message": "Red-flag record deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Red-flag record not found"}), 404)
        
    
    # intervention records route
class InterventionRecordResource(Resource):

        # get all intervention records
    def get(self):
        
        intervention_flags = [intervention.to_dict() for  intervention in InterventionRecord.query.all()]
        if intervention_flags:
            return make_response(jsonify(intervention_flags),200)
        else:
             return make_response(jsonify({"error": "There are no intervention records"}), 404)

        # post an intervention record.
    def post(self):
        data = request.get_json()

        title=data.get('title')
        description=data.get('description')
        image = data.get('image')
        video = data.get('video')
        location = data.get('location')
        status = data.get('status')
        user_id=data.get('user_id')

        if title and description and status and location:
            new_intervention = InterventionRecord(title=title, description=description, image=image, video=video, location=location, status=status, user_id=user_id)

            db.session.add(new_intervention)
            db.session.commit()
      
            return make_response(jsonify(new_intervention.to_dict(), 200))
        
        return make_response(jsonify({"error": "Intervention details must be added"}), 422)
    
class InterventionRecordById(Resource):
    def get(self,id):
        record=InterventionRecord.query.filter_by(id=id).first().to_dict()

        if record:
            return make_response(jsonify(record),200)
        
        return make_response(jsonify({"error": "Intervention record not found"}), 404)
    
        # edit an intervention record
    def patch(self, id):
        intervention = InterventionRecord.query.filter_by(id=id).first()

        if intervention:
            for attr in request.get_json():
                setattr(intervention,attr,request.get_json()[attr])

                db.session.add(intervention)
                db.session.commit()

                user = User.query.get(intervention.user_id)
                if user:
                    email_on_status_change(user.email,intervention.title,intervention.status)
            return make_response(jsonify(intervention.to_dict(), 200)) 
        
        
        return make_response(jsonify({"error": "Intervention record not found"}), 404)

        # delete an intervention record from the system
    def delete(self, id):
        intervention = InterventionRecord.query.filter_by(id=id).first()

        if intervention:
            db.session.delete(intervention)
            db.session.commit()
            return make_response(jsonify({"message": "Intervention record deleted successfully"}), 200)
        else:
            return make_response(jsonify({"error": "Intervention record not found"}), 404)



api.add_resource(Index,'/', endpoint='landing')
api.add_resource(UserResource, '/users', endpoint='users')
api.add_resource(UserById,'/user/<int:id>')
api.add_resource(AdminResource, '/admins', endpoint='admins')
api.add_resource(RedFlagRecordResource, '/redflags', endpoint='redflags')
api.add_resource(RedFlagRecordById,'/redflags/<int:id>', endpoint='redflags_id')
api.add_resource(InterventionRecordResource, '/intervention', endpoint='intervention')
api.add_resource(InterventionRecordById, '/intervention/<int:id>', endpoint='interventbyid')
api.add_resource(SignupUser, '/signup_user', endpoint='signup')
api.add_resource(LoginUser, '/login_user', endpoint='login')
api.add_resource(CheckUser,'/session_user',endpoint='session_user' )
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(AddAdmin, '/add_admin', endpoint='add_admin')
api.add_resource(LoginAdmin, '/login_admin', endpoint='login_admin')
api.add_resource(CheckAdmin,'/session_admin',endpoint='session_admin')
api.add_resource(LogoutAdmin, '/logoutA', endpoint='logout_admin')




@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({"error": "Not Found: The requested endpoint (resource) does not exist"}),
        404
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

