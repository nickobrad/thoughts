from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime, date

@login_manager.user_loader
def load_user(userName):
    return User.query.get(str(userName))

class User(UserMixin, db.Model):

    def get_id(self):
        return (self.username)

    __tablename__ = 'users'

    username = db.Column(db.String(255),unique = True, primary_key = True)
    firstname = db.Column(db.String(255))
    secondname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index = True) 
    profile_picture = db.Column(db.String())
    profile_bio = db.Column(db.String(255))
    secured_password = db.Column(db.String(255))
    pitches = db.relationship('Pitch', backref = 'moto', lazy = 'dynamic')
    commentsByMe = db.relationship('PitchComment', backref = 'userzs', lazy = 'dynamic')
    
    @property
    def password(self):
        raise AttributeError('You cannot view a users password')

    @password.setter
    def password(self, password):
        self.secured_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secured_password, password)

class Category(db.Model):
    __tablename__ = 'cats'

    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(255))
    pitch = db.relationship('Pitch', backref = 'categ', lazy = "dynamic")
    


class Pitch(db.Model):
    __tablename__ = 'pitch' 

    id = db.Column(db.Integer, primary_key = True)
    pitch = db.Column(db.String) 
    categoryOfPitch = db.Column(db.Integer, db.ForeignKey("cats.id"))
    date_posted = db.Column(db.DateTime, default = date.today)
    user = db.Column(db.String, db.ForeignKey("users.username"))
    upvote = db.Column(db.Integer, default = 0)
    downvote = db.Column(db.Integer, default = 0)
    comments = db.relationship('PitchComment', backref = 'pitch', lazy = "dynamic")

    def save_pitch(self):
        db.session.add(self) 
        db.session.commit()

    def delete_pitch(self):
        db.session.delete(self)
        db.sesion.commit()

    @classmethod
    def pitch_by_id(cls, id):
        pitches = Pitch.query.filter_by(id = id).first()
        return pitches

    @classmethod
    def all_pitches(cls, inputUserName):
        pitches = Pitch.query.filter_by(user = inputUserName).all()
        return pitches

class PitchComment(db.Model):
    __tablename__ = 'pitchcomments'

    id = db.Column(db.Integer, primary_key = True)
    pitch_id = db.Column(db.Integer, db.ForeignKey("pitch.id"))
    comment = db.Column(db.String)
    user = db.Column(db.String, db.ForeignKey("users.username"))
    date_posted = db.Column(db.DateTime, default = date.today)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.sesion.commit()

    @classmethod
    def all_comments(cls, inputUser):
        comments = PitchComment.query.filter_by(user = inputUser).all()
        return comments



