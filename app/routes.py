from flask import render_template, flash, redirect,url_for,request
from flask_login import current_user, login_user, logout_user
from app.models import UserProfile
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
        print(form.dob.data)
        user = UserProfile(fname=form.fname.data,lname=form.lname.data,email=form.email.data)
        user.set_password(form.password.data)
        user.set_dob(form.dob.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('signin'))
    return render_template('sign-up.html', title='Sign-Up - Mealicious', form=form)