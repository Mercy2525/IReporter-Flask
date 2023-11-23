from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    

    red_flag_records = db.relationship('RedFlagRecord', backref='user')
    intervention_records = db.relationship('InterventionRecord', backref='user')

    serialize_rules=('-red_flag_records.user','-intervention_records.user',)


class Admin(db.Model,SerializerMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))


class RedFlagRecord(db.Model,SerializerMixin):
    __tablename__ = 'redFlagRecords'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    video = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules=('-user.red_flag_records',)


class InterventionRecord(db.Model,SerializerMixin):
    __tablename__ = 'intervention_records'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    video = db.Column(db.String(100))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules=('-user.intervention_records',)
