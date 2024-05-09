#user and blog post models

#database is setup in the __init__.py file
from blogwebsite import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin   #we will use functionalities like isAuthenticated, isAnonymous, etc.
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):  #allows us to do is_authenticated, is_anonymous, etc. in our template
    return User.query.get(user_id)

class User(db.Model, UserMixin):  #usermixin allows us to use login manager functionalities
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    profile_image=db.Column(db.String(64), nullable=False, default='default_profile.png')  #nullable means if users dont provide image we will give them a default one
    email=db.Column(db.String(64), unique=True, index=True)
    username=db.Column(db.String(64), unique=True, index=True) #index sets up an index
    password_hash=db.Column(db.String(128))

    posts=db.relationship('BlogPost', backref='author', lazy=True)  #one to many relationship, user can have many blog posts

    def __init(self, email, username, password):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):    #method to check password using login
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"
    

class BlogPost(db.Model):
    users=db.relationship(User)
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  #setting up foreign key
    date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title=db.Column(db.String(40), nullable=False)
    text=db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title=title
        self.text=text
        self.user_id=user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- Title: {self.title}"