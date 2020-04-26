from flask import render_template, flash, redirect,url_for,request,jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import UserProfile,Mealplan,MealplanDetail,MealInfo
from werkzeug.urls import url_parse
import time

from app import app,db
from app.forms import LoginForm,RegistrationForm

#Index Page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home - Mealicious')

#Sign In Page
@app.route('/sign-in',methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Email Address Or Password==alert-danger")
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('sign-in.html', title='Sign In - Mealicious', form=form)

#Sign Out Page
@app.route('/sign-out')
def signout():
    logout_user()
    return redirect(url_for('index'))

#Sign Up Page
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserProfile(fname=form.fname.data,lname=form.lname.data,email=form.email.data,weight=form.weight.data,profession=form.profession.data)
        user.set_password(form.password.data)
        user.set_dob(form.dob.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!==alert-success')
        return redirect(url_for('signin'))
    return render_template('sign-up.html', title='Sign-Up - Mealicious', form=form)

#Contact Us Page
@app.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    return render_template('contact-us.html', title='Contact Us - Mealicious')

#Browse Meals Page
@app.route('/browse-meals', methods=['GET', 'POST'])
def browse_meals():
    return render_template('browse-meals.html', title='Browse Meals - Mealicious')

#Meet the Team Page
@app.route('/meet-team', methods=['GET', 'POST'])
def meet_team():
    return render_template('team-page.html', title='Meet The Team - Mealicious')

#Admin Page
@app.route('/admin', methods=['GET', 'POST'])
@login_required #To protect from users who are not authenticated
def admin():
    user_id = current_user.user_id
    mealplan = Mealplan.query.all()
    mealplan_detail = MealplanDetail.query.all()
    meals =  MealInfo.query.filter(MealInfo.meal_id != 0).all()
    userprofile = UserProfile.query.all()
    return render_template('admin.html', title='Admin - Mealicious',mealplans=mealplan,mealplan_details=mealplan_detail,meals=meals,userprofile=userprofile)


#Create Mealplan Page
@app.route('/create-mealplan', methods=['GET', 'POST'])
@login_required #To protect from users who are not authenticated
def create_mealplan():
    user_id = current_user.user_id
    days = ['sun','mon','tue','wed','thu','fri','sat']
    mealplans_view = []
    for day in days:
        mealplandic = {}
        mealplandic[day] = [{'mealtype':'bf','meal_id':0,'meal_name':'','meal_cal':0},
        {'mealtype':'lun','meal_id':0,'meal_name':'','meal_cal':0},
        {'mealtype':'din','meal_id':0,'meal_name':'','meal_cal':0}]
        mealplans_view.append(mealplandic)
    #Get Mealplan Names and Meals from the Database
    mealnames = MealInfo.query.filter(MealInfo.meal_id != 0).all()
    mealplannames = Mealplan.query.distinct(Mealplan.week_date,Mealplan.mealplan_name).filter(Mealplan.status == 'Y').filter(Mealplan.user_id == user_id).all()
    if request.method == 'POST' and request.json['option']=='create_mealplan':
        #Create the Mealplan
        mealplan_name = request.json['mealplanName']
        mealplan_week = request.json['mealplanWeek']
        mealplans = request.json['mealplanobj']
        for key,value in mealplans.items():
            dayname = key
            totalcal = mealplans[dayname]['totalcal']
            mealplan = Mealplan(mealplan_name=mealplan_name,user_id=user_id,
            week_date=mealplan_week,day_name=dayname,total_daily_cal=totalcal,status='Y')
            db.session.add(mealplan)
            db.session.flush()
            mealplan_id = mealplan.mealplan_id
            bfmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['b']['meal_id'],meal_type='b')
            lunmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['l']['meal_id'],meal_type='l')
            dinmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['d']['meal_id'],meal_type='d')
            #Insert Data into Database
            db.session.add(bfmeal)
            db.session.add(lunmeal)
            db.session.add(dinmeal)
            db.session.commit()
        flash('Congratulations, Your Mealplan is Created Successfully.==alert-success')
        return jsonify({'status':"Congratulations, Your Mealplan is Created Successfully. Please wait while the page reloads.....","Response":1})
    elif(request.method == 'POST' and request.json['option']=='view_mealplan'):
        #View an Exisiting Mealplan
        mealplan_name = request.json['mealplanName']
        mealplan_week = request.json['mealplanWeek']
        viewplans = db.session.query(MealInfo.meal_id,MealInfo.meal_name,MealInfo.cal_count,MealplanDetail.meal_type,Mealplan.day_name).join(Mealplan.mealplandetails).join(MealInfo).filter(Mealplan.mealplan_name == mealplan_name).filter(Mealplan.week_date == mealplan_week).filter(Mealplan.user_id == user_id).filter(Mealplan.status == 'Y').all()
        return jsonify({'status':"View Meal Plans","Response":viewplans})
    elif(request.method == 'POST' and request.json['option']=='delete_mealplan'):
        #Delete the Selected Mealplan
        mealplan_name = request.json['mealplanName']
        mealplan_week = request.json['mealplanWeek']
        db.session.query(Mealplan).filter(Mealplan.mealplan_name == mealplan_name).filter(Mealplan.week_date == mealplan_week).filter(Mealplan.user_id == user_id).update({Mealplan.status: 'N'}, synchronize_session=False)
        db.session.commit()
        flash('Mealplan "'+mealplan_name+'" is deleted  successfully.==alert-success')
        return jsonify({'status':"MealPlan deleted","Response":1})
    return render_template('create-mealplan.html', title='Create Mealplan - Mealicious',mealplans=mealplans_view,mealnames=mealnames,mealplannames=mealplannames)
