from app import app
from models import db, User, Admin, RedFlagRecord, InterventionRecord
from faker import Faker
from random import choice as rc

fake=Faker()

with app.app_context():
    User.query.delete()
    Admin.query.delete()
    RedFlagRecord.query.delete()
    InterventionRecord.query.delete()

    print('deleting existing data_bases')

    admins=[]

    for i in range(2):
        admin=Admin(full_name=fake.name(), username=fake.user_name())

        admins.append(admin)
        db.session.add_all(admins)
        db.session.commit()

    print('generating admins')

    users=[]

    for i in range(10):
        user=User(full_name=fake.name(), email=fake.email(), username=fake.user_name())

        users.append(user)
        db.session.add_all(users)
        db.session.commit()

    print('generating users')

    red_flags=[]

    for i in range(10):
        red_flag=RedFlagRecord(
            image=fake.url(), video=fake.url(),
            location=fake.text(10), status=rc(['Pending','Under Investigation','Resolved']), user=rc(users)
            )
        
        red_flags.append(red_flag)
        db.session.add_all(red_flags)
        db.session.commit()
        
    print('generating red_flag records')

    interventions=[]

    for i in range(10):
        intervention=InterventionRecord(
            image=fake.url(), video=fake.url(),
            location=fake.text(10), status=rc(['Pending','Under Investigation','Resolved']), user=rc(users)
            )
        
        interventions.append(intervention)
        db.session.add_all(interventions)
        db.session.commit()
        
    print('generating intervention records')

    print('done seeding...')

    