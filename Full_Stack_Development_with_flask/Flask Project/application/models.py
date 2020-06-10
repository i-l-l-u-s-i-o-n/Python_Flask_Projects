import flask
from application import db
# Mongo DB models
class User(db.Document):
    user_id       =       db.IntField(unique=True)
    first_name    =       db.StringField( max_length=50)
    last_name     =       db.StringField( max_length=50)
    email         =       db.StringField( max_length=50)
    password      =       db.StringField( max_length=50)

class Course(db.Document):
    course_id =     db.StringField(max_length=10,unique=True) 
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=255)
    credits = db.IntField()
    term = db.StringField(max_length=25)


# This is like many to many relationship. 1 student can enroll to many subjects and 1 subject or course can be enrolled by many students
class Enrollment(db.Document):
    course_id =     db.StringField(max_length=10,unique=True) 
    user_id = db.IntField()