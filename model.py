from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, BLOB,desc,asc, Boolean
from sqlalchemy.sql.expression import true
from config import setup_app

db = SQLAlchemy(setup_app())

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    middlename = Column(String)
    lastname = Column(String)
    studentid = Column(Integer,unique=True)
    email = Column(String,unique=True)
    password = Column(String)
    access = Column(String)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    image = Column(String)
    image_description = Column(String,default='')
    content = Column(Text)
    suggested_by = Column(String,default='SSU - SSG')
    date = Column(DateTime)
    slug=Column(String,unique=True)

class Message(db.Model):
    __tablename__ = 'message'
    id = Column(Integer,primary_key=True)
    studentid = Column(Integer)
    message = Column(String)
    reply = Column(String)
    date = Column(DateTime)

class BulletinSuggestion(db.Model):
    __tablename__ = 'bulletin_suggestion'
    id = Column(Integer,primary_key=True)
    requestee = Column(String)
    message = Column(String)
    date = Column(DateTime)
    approved = Column(Boolean,default=False)


class BulletinConcerns(db.Model):
    __tablename__ = 'bulletin_concerns'
    id = Column(Integer,primary_key=True)
    requestee = Column(String)
    message = Column(String)
    image = Column(String)
    date = Column(DateTime)
    approved = Column(Boolean,default=False)
