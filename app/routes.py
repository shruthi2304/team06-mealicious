from flask import render_template, flash, redirect,url_for,request,jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app.models import UserProfile,Mealplan,MealplanDetail,MealInfo
from werkzeug.urls import url_parse

from app import app,db
from app.forms import LoginForm,RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home - Mealicious')

@app.route('/sign-in',methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Email Address Or Password")
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('sign-in.html', title='Sign In - Mealicious', form=form)

@app.route('/sign-out')
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserProfile(fname=form.fname.data,lname=form.lname.data,email=form.email.data)
        user.set_password(form.password.data)
        user.set_dob(form.dob.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('signin'))
    return render_template('sign-up.html', title='Sign-Up - Mealicious', form=form)


@app.route('/create-mealplan', methods=['GET', 'POST'])
@login_required #To protect from users who are not authenticated
def create_mealplan():
    days = [{'abbr':'sat'},{'abbr':'sun','name':'Sunday'},{'abbr':'mon','name':'Monday'},
    {'abbr':'tue','name':'Tue'},{'abbr':'wed','name':'Wednesday'},{'abbr':'thu','name':'Thursday'},
    {'abbr':'fri','name':'Friday'}]
    meals = [{'mealabbr':'bf'},{'mealabbr':'lun'},{'mealabbr':'din'}]
    mealnames = MealInfo.query.filter(MealInfo.meal_id != 0).all()
    if request.method == 'POST':
        user_id = current_user.user_id
        mealplan_name = request.json['mealplanName']
        mealplan_week = request.json['mealplanWeek']
        mealplans = request.json['mealplanobj']
        for key,value in mealplans.items():
            dayname = key
            totalcal = mealplans[dayname]['totalcal']
            mealplan = Mealplan(mealplan_name=mealplan_name,user_id=user_id,
            week_date=mealplan_week,day_name=dayname,total_daily_cal=totalcal)
            db.session.add(mealplan)
            db.session.flush()
            mealplan_id = mealplan.mealplan_id
            bfmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['b']['meal_id'],meal_type='b')
            lunmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['l']['meal_id'],meal_type='l')
            dinmeal = MealplanDetail(mealplan_id=mealplan_id,meal_id=mealplans[dayname]['d']['meal_id'],meal_type='d')
            db.session.add(bfmeal)
            db.session.add(lunmeal)
            db.session.add(dinmeal)
            db.session.commit()
        return jsonify({'status':"Meal Plan Created Successfully"})
    return render_template('create-mealplan.html', title='Create Mealplan - Mealicious',days=days,meals=meals,mealnames=mealnames)
