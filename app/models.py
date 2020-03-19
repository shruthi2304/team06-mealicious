from datetime import datetime
from app import db,login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UserProfile(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(64), index=True)
    lname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dob = db.Column(db.DateTime,default=datetime.now())
    weight = db.Column(db.Integer)
    profession = db.Column(db.String(80))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {} {}, {} >'.format(self.fname,self.lname,self.dob)
    
    def get_id(self):
           return (self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

    def set_dob(self,dob):
        dob_arr = dob.split("-")
        self.dob = datetime(int(dob_arr[0]),int(dob_arr[1]),int(dob_arr[2]),0,0,0)

@login.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))