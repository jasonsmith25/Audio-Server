from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime
import pathlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.sqlite3'
db = SQLAlchemy(app)

UPLOAD_FOLDER = str(pathlib.Path().absolute()) + '/audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("connected")

class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Float, default=0, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = (CheckConstraint(duration >= 0, name='check_duration_positive'),{})

class Podcast(db.Model):
    __tablename__ = "podcast"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Float, default=0, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.now())
    host = db.Column(db.String(100), nullable=True)
    paticipant = db.Column(db.String(100), nullable=True)
    __table_args__ = (CheckConstraint(duration >= 0, name='check_duration_positive'),{})

class Audiobook(db.Model):
    __tablename__ = "audiobook"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    narrator = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Float, default=0, nullable=False)
    uploaded_time = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = (CheckConstraint(duration >= 0, name='check_duration_positive'),{})
