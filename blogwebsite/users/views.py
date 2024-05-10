#users/views.py
#we will need views to - register, login, logout, account(update user), user's list of blogs

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blogwebsite import db
from blogwebsite.models import User, Blog
from blogwebsite.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blogwebsite.users.picture_handler import add_profile_pic

users=Blueprint('users', __name__)

#logout view
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))  #redirecting to home page #core is the blueprint name in blogwebsite/core/views.py

@users.route('register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)

@users.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None: #check_password is a method in models.py
            login_user(user)  #inbuilt function that logs in the user automatically
            flash('Logged in successfully!')
            next=request.args.get('next')  #if the user was trying to access a page that required login, it will redirect to that page after login
            if next==None or not next[0]=='/':
                next=url_for('core.index')
            
            return redirect(next)
    
    return render_template('login.html', form=form)