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

#register view
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

#login view
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


#account view (update user)
@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:  #if user uploads a picture
            username=current_user.username #get the username of the current user
            pic = add_profile_pic(form.picture.data, username) #add_profile_pic is a function in picture_handler.py #it returns the picture file name
            current_user.profile_image=pic #profile_image is a attribute in models.py user table  #storage_filename is the file name which is now stored in the user's profile_image attribute

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    
    elif request.method=='GET':  #they are not submitting the form, they are just trying to get the form
        form.username.data=current_user.username
        form.email.data=current_user.email

    profile_image=url_for('static', filename='profile_pics/'+current_user.profile_image) #what we are doing here is we are getting the profile image of the current user and displaying it in the account page
    return render_template('account.html',profile_image=profile_image,form=form)


