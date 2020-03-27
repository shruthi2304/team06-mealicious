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
    mealplans = db.relationship('Mealplan', backref='usermeal', lazy='dynamic')

    def __repr__(self):
        return '<UserProfile {} {}, {} >'.format(self.fname,self.lname,self.dob)
    
    def get_id(self):
           return (self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

    def set_dob(self,dob):
        dob_arr = dob.split("-")
        self.dob = datetime(int(dob_arr[0]),int(dob_arr[1]),int(dob_arr[2]),0,0,0)

class MealInfo(db.Model):
    meal_id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(64), index=True)
    cal_count = db.Column(db.Integer)
    meals = db.relationship('MealplanDetail', backref='mealsinf', lazy='dynamic')

    def __repr__(self):
        return '<MealInfo {}, {}, {} >'.format(self.meal_id,self.meal_name,self.cal_count)

class Mealplan(db.Model):
    mealplan_id = db.Column(db.Integer, primary_key=True)
    mealplan_name = db.Column(db.String(100),index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'))
    week_date = db.Column(db.String(64),index=True)
    day_name = db.Column(db.String(3),index=True) 
    total_daily_cal = db.Column(db.Integer)
    mealplandetails = db.relationship('MealplanDetail', backref='mealplaninf', lazy='dynamic')

    def __repr__(self):
        return '<Mealplan {}, {}, {} >'.format(self.user_id,self.week_no,self.day_no)

class MealplanDetail(db.Model):
    mealplandetail_id = db.Column(db.Integer, primary_key=True)
    mealplan_id = db.Column(db.Integer, db.ForeignKey('mealplan.mealplan_id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal_info.meal_id'))
    meal_type = db.Column(db.String(1), index=True)

    def __repr__(self):
        return '<MealplanDetail {}, {}, {} >'.format(self.mealplan_id,self.meal_id,self.meal_type)


@login.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
