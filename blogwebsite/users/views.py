#users/views.py
#we will need views to - register, login, logout, account(update user), user's list of blogs

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blogwebsite import db
from blogwebsite.models import User, BlogPost
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

#user's list of blogs
@users.route('/<username>') #<> is a dynamic part of the url and username changes depending on the user
def user_posts(username):
    page=request.args.get('page',1,type=int)  #what happens here is if the user is on page 1, it will show the first 5 blogs, if the user is on page 2, it will show the next 5 blogs and so on

    users=User.query.filter_by(username=username).first_or_404()  #if the user does not exist, it will show a 404 error
    blog_post = BlogPost.query.filter_by(author=users).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)  #getting the blog posts of the user #author is the attribute in the blogpost table in models.py backref='author' #date is the attribute in the blogpost table in models.py and desc is used to show the latest blog first
    #paginate is used to show only 5 blogs per page

    return render_template('user_blog_posts.html', blog_post=blog_post, users=users)  #users is the user whose blog posts we are displaying

