#holds organization of the application like connecting blueprints, and everything together, etc.
#blogwebsite/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  #for security purposes

#setting up the database
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)
#setup context **IMPORTANT**
app.app_context().push()

#setting up login manager
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view('users.login')   #telling users where to go to login



#registering core blueprint
from blogwebsite.core.views import core
#registering error_pages blueprint
from blogwebsite.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(error_pages)
#registering users blueprint
from blogwebsite.users.views import users
app.register_blueprint(users)